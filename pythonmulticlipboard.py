# Step 1: Comments and shelf setup

# mcb.pyw - Saves and loads pieces of text to the clipboard.
# Usage: py.exe mcb.pyw save <keyword> - Saves clipboard to keyword.
# py.exe mcb.pyw <keyword> - Loads keyword to clipboard.
# py.exe mcb.pyw list - Loads all keywords to clipboard.

import shelve, pyperclip, sys
mcbShelf = shelve.open('mcb')

# TODO: Save clipboard content.
# TODO: List keywords and load content.
mcbShelf.close()

# Step 2: Save clipboard content with a clipboard

if len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
    mcbShelf[sys.argv[2]] = pyperclip.paste()
    print(f"Saved clipboard content under the key '{sys.argv[2]}'")

# Step 3: List keywords and load content
elif len(sys.argv) == 2:
    if sys.argv[1].lower() == 'list':
        # List all keywords
        pyperclip.copy(str(list(mcbShelf.keys())))
        print("Keywords copied to clipboard")
    elif sys.argv[1] in mcbShelf:
        # Load content for a specific keyword
        pyperclip.copy(mcbShelf[sys.argv[1]])
        print(f"Copied content from key '{sys.argv[1]}' to clipboard")
    else:
        print(f"No content found under the key '{sys.argv[1]}'")

mcbShelf.close()