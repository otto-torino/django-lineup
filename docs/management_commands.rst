=====
Management Commands
=====

Django Lineup provides a management command you can use to import a JSON formatted menu from file ::

    $ python manage.py import_menu_from_json /path/to/menu.json

The file should contain a JSON representation of the menu, i.e. ::

    {
      "label": "Main Menu",
      "slug": "main-menu",
      "order": 0,
      "children": [
        {
          "label": "Tools",
          "slug": "tools",
          "order": 0,
          "children": [
            {
              "label": "DNS Tools",
              "slug": "dns-tools",
              "order": 0,
              "login_required": true,
              "children": [
                {
                  "label": "DMARC DNS Tools",
                  "slug": "dmarc-dns-tools",
                  "link": "/dmarc-tools/",
                  "title": "DMARC Rulez",
                  "order": 0
                }
              ]
            },
            {
              "label": "Password Generator",
              "slug": "password-generator",
              "order": 1
            }
          ]
        },
        {
          "label": "Disabled Item",
          "slug": "disabled-item",
          "order": 1,
          "enabled": false,
          "children": [
            {
              "label": "Disabled child",
              "slug": "disabled-child",
              "order": 0
            }
          ]
        },
        {
          "label": "Perm Item",
          "slug": "perm-item",
          "order": 2,
          "permissions": [
            "add_permission",
            "view_session"
          ]
        }
      ]
    }
