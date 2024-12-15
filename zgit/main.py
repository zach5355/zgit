import sys
import os
import zlib
import hashlib

def main():
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        # arg2 is -p going to ignore that for now
        if len(sys.argv) == 4:
            hash = sys.argv[3]
        else:
            hash = sys.argv[3]
        folder = hash[:2]
        file = hash[2:]
        path = os.path.join(os.getcwd(),".git","objects",folder,file)
        file = open(path,'rb')
        file_contents = file.read()
        
        uncompressed = zlib.decompress(file_contents)
        header,content = uncompressed.split(b"\0",maxsplit=1)

        print(content.decode(encoding="utf-8"),end="")
        file.close()
        
    elif command =="hash-object":
        print(len(sys.argv))
        file_name = ""
        writeFile = False
        if len(sys.argv) > 3:
            file_name = sys.argv[3]
            if(sys.argv[2] == "-w"):
                writeFile = True
        else:
            file_name = sys.argv[2]
        #compute SHA hash of file uncompressed
        #the SHA input is the header and the uncompressed data
        # blob <size>\0 <content>
        path = os.path.join(os.getcwd(),file_name)
        file = open(path,"rb")
        file_content = file.read()
        file.close()
        header = f"blob {len(file_content)}\x00"
        store_file = header.encode("utf-8") + file_content
        hash = hashlib.sha1(store_file).hexdigest()
        print(hash)
        #if write, then write it to .git/objects
        # contents of the file will be compressed with zlip
        if writeFile:
            print("writing file")
            compressed_contents = zlib.compress(store_file)
            blob_directory = os.path.join(os.getcwd(),".git","objects",hash[:2])
            blob_path = os.path.join(os.getcwd(),".git","objects",hash[:2],hash[2:])
            os.makedirs(blob_directory,exist_ok=True)
            with open(blob_path,"wb") as blob_file:
                #failing due to everything on pc being locked in readonly I think
                blob_file.write(compressed_contents)
                blob_file.close()


    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
