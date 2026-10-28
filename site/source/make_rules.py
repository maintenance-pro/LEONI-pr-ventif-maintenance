"""Write database.rules.json (Firebase Realtime Database) for the Firebase build.

owner  = the manager (meta/owner, locked to his uid)
admin  = owner, or an approved account with role admin
editor = owner, or an approved account with role tl / admin (may change the planning)
member = owner, an approved account, or a technician whose matricule is in techMats (matricule-only login)
"""
import json
import pathlib

OWNER_UID = "dqDCiVUUnoUS9S1T0gRkPh6BRwt1"
MAT_DOMAIN = "@matricule.example.com"

owner = "root.child('meta/owner').val() === auth.uid"
ok = "root.child('users/' + auth.uid + '/ok').val() === true"
role = "root.child('users/' + auth.uid + '/role').val()"
tech = (f"(auth.token.email != null && auth.token.email.endsWith('{MAT_DOMAIN}') && "
        f"root.child('techMats/' + auth.token.email.replace('{MAT_DOMAIN}', '')).exists())")
admin = f"({owner} || ({ok} && {role} === 'admin'))"
editor = f"({owner} || ({ok} && ({role} === 'tl' || {role} === 'admin')))"
member = f"({owner} || {ok} || {tech})"
A = "auth != null && "
self_ = "auth != null && auth.uid === $uid"
by_admin_not_self_owner = f"auth != null && auth.uid !== $uid && $uid !== root.child('meta/owner').val() && {admin}"
role_ok = "newData.val() === 'tech' || newData.val() === 'tl' || newData.val() === 'admin'"

rules = {"rules": {
    "meta": {
        ".read": "auth != null",
        "owner": {".write": f"auth != null && !data.exists() && newData.val() === auth.uid && auth.uid === '{OWNER_UID}'"},
    },
    "users": {
        ".read": A + member,
        "$uid": {
            ".read": self_,
            ".write": f"!newData.exists() && {by_admin_not_self_owner}",  # compte supprimé par un admin
            "nom": {".write": f"{self_} || ({by_admin_not_self_owner})", ".validate": "newData.isString() && newData.val().length <= 80"},
            "ident": {".write": self_, ".validate": "newData.isString() && newData.val().length <= 120"},
            "at": {".write": self_, ".validate": "newData.isString() && newData.val().length <= 40"},
            "demande": {".write": self_, ".validate": role_ok},
            "tech": {".write": self_, ".validate": "newData.isBoolean()"},
            "ok": {".write": by_admin_not_self_owner, ".validate": "newData.isBoolean()"},
            "role": {".write": by_admin_not_self_owner, ".validate": role_ok},
            "fin": {".write": by_admin_not_self_owner, ".validate": "newData.isString() && newData.val().length <= 40"},
            "tlName": {".write": by_admin_not_self_owner, ".validate": "newData.isString() && newData.val().length <= 80"},
            "del": {".write": by_admin_not_self_owner, ".validate": "newData.isBoolean()"},  # supprimé, gardé pour ses modifications du planning
            "$other": {".validate": False},
        },
    },
    "techMats": {  # matricules autorisés : tenus à jour par un admin ou un TL (techniciens ajoutés par le TL)
        ".read": A + editor,
        ".write": A + editor,
        "$mat": {
            ".read": f"auth != null && auth.token.email === $mat + '{MAT_DOMAIN}'",
            ".validate": "newData.hasChildren(['nom']) && newData.child('nom').isString() && newData.child('nom').val().length <= 80",
        },
    },
    "helperKey": {  # clé de l'IA (HELPER, lecture des standards) : enregistrée par un admin, lue par les comptes autorisés
        ".read": A + member,
        ".write": A + admin,
        "k": {".validate": "newData.isString() && newData.val().length >= 20 && newData.val().length <= 300 && newData.val().matches(/^[A-Za-z0-9_.-]+$/)"},  # Google AIza… ou Anthropic sk-ant-…
        "at": {".validate": "newData.isString() && newData.val().length <= 40"},
        "p": {".validate": "newData.val() === 'gemini' || newData.val() === 'claude'"},
        "$other": {".validate": False},
    },
    "helperUse": {  # nombre de questions posées à HELPER, par personne et par jour
        ".read": A + admin,
        "$uid": {
            ".read": "auth != null && auth.uid === $uid",
            "$day": {
                ".write": f"auth != null && auth.uid === $uid && {member}",
                ".validate": "newData.isNumber() && newData.val() >= 0 && newData.val() <= 10000 && $day.matches(/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/)",
            },
        },
    },
    "suivi": {".read": A + member, "$mid": {".write": A + member}},
    "config": {".read": A + member, ".write": A + admin,
               "org": {".write": A + editor},  # organisation : les TL modifient aussi leurs sections (l'écran limite aux leurs)
               "std": {".write": A + editor}},  # standards préventifs : aussi le TL (ses sections)
    # archives des plannings : créées par un admin ou un TL (jamais modifiées), supprimées par un admin
    "archives": {".read": A + editor, "$id": {".write": f"auth != null && ((!data.exists() && newData.exists() && {editor}) || (!newData.exists() && {admin}))"}},
    "archIdx": {".read": A + editor, "$id": {".write": f"auth != null && ((!data.exists() && newData.exists() && {editor}) || (!newData.exists() && {admin}))",
                                             ".validate": "newData.hasChildren(['at', 'svc', 'year', 'week'])"}},
    "reqs": {".read": A + member, "$uid": {".write": f"auth != null && auth.uid === $uid && {ok}"}},
    "modifs": {".read": A + member, "$uid": {".write": f"auth != null && auth.uid === $uid && {editor}"}},
}}

out = pathlib.Path(__file__).parent / "database.rules.json"
out.write_text(json.dumps(rules, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, out.stat().st_size, "bytes")
