# manifestGuard

- A script to make AndroidManifest.xml can not be decompiled by jadx or apktool but can run on Andorid system. 

## useage

- guard mode:

  ```
  python .\manifestGuard.py -g -s ./AndroidManifestori.xml -o ./AndroidManifest.xml 
  ```

- fixed mode:

  ```
  python .\manifestGuard.py -f -s ./AndroidManifestori.xml -o ./AndroidManifestnew.xml
  ```