# manifestGuard

- A script to make AndroidManifest.xml can not be decompiled by jadx or apktool but can run on Android system. 

- like this:

  ![image](https://github.com/Sp1keeeee/manifestGuard/blob/main/IMG/jadx.png)

- [https://bbs.pediy.com/thread-275427.htm#msg_header_h2_0](https://bbs.pediy.com/thread-275427.htm#msg_header_h2_0)

## useage

- guard mode:

  ```
  python .\manifestGuard.py -g -s ./AndroidManifestori.xml -o ./AndroidManifest.xml 
  ```

- fixed mode:

  ```
  python .\manifestGuard.py -f -s ./AndroidManifestori.xml -o ./AndroidManifestnew.xml
  ```