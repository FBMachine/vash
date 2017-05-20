## VASH - Virtual Api SHell
Install and use REST APIs and grpc servers as if they were local resources.

```bash
~$ chmod +x vash
~$ ./vash
 __   ___   ___ _  _
 \ \ / /_\ / __| || |
  \ V / _ \\__ \ __ |
   \_/_/ \_\___/_||_|

~$ ls
~$ install examples/petstore
~$ ls
petstore
~$ cd petstore
~/petstore$ ls
user
store
pet
pet
user

~/petstore$ cd store
~/petstore/store$ ls
order
inventory
~/petstore/store$ inventory
{...} # <- result of get request to: http://petstore.swagger.io/v2/store/inventory
~/petstore/store$ exit
```
