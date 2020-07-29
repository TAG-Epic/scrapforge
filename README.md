# Scrapforge
Collection of tools to install/distribute scrap mechanic survival mods

## How to install a mod
run `python3 main.py install <modfile>`

## How to package your mod
Create a folder with the name of your mod
Add a mod.info file (json syntax) like this
```json
{
    "name": "examplemod"
}
```
Create a folder named patches
Put all your patches in the patches folder
Zip the folder
Change the extension to .scrapforge
