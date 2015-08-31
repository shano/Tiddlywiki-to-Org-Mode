# Converting tiddlywiki to org mode

# Open folder of files
import glob,re
import ntpath

tiddlyPath = '/home/user/Documents/tiddlywiki/tiddlers/*.tid'
orgPath = '/home/user/Documents/Org/'


def main():
    count = 0
    # Iterate over each file
    for file in glob.glob(tiddlyPath):
        with open(file) as fr:
            count += 1
            TAGS = ''
            TITLE = ''
            # Ignore the sys files
            if ntpath.basename(file).startswith('$__'):
                continue

            output = ''
            for line in fr.readlines():
                # Remove created: ,modified: and type: lines
                if line.startswith('created:'):
                    continue
                if line.startswith('modified:'):
                    continue
                if line.startswith('type:'):
                    continue

                # Append any tags to the headline
                if line.startswith('tags:'):
                    if line[5:].strip():
                        TAGS = line[5:].replace(' ',':')
                    continue

                # Take title and put it as tagline at the top of the page as a headline
                if line.startswith('title:'):
                    TITLE = line[7:-1]
                    output += '* ' + TITLE
                    if TAGS:
                        output += '                       ' + TAGS
                    output += '\n'
                    continue

                # Convert any lines in the file starting with ! to **
                if line.startswith('!!'):
                    output += line.replace(' ','').replace('!!', '*** ', 1)
                    continue
                elif line.startswith('!'):
                    output += line.replace(' ','').replace('!', '** ', 1)
                    #output += '** ' + line[1:] + '\n'
                    continue

                # Convert internal links to correct format
                output += re.sub(r'\[\[(.+?)\]\]', r'[[file:%s\1.org][\1]]' % orgPath, line)

            # write file
            fw = open(orgPath + TITLE.replace('/','') + '.org' ,'w')
            fw.write(output)
            fw.close()
    print('Converted %d tid files to org format' % count)

if __name__ == "__main__":
    main()
