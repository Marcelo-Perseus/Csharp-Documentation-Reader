import codecs
import sqlite3

# First, open up the database
conn = sqlite3.connect("Projects/C# Documentation Scraper/database.db")
cur = conn.cursor()

class OutlineElement():
    def __init__(self, _id:str="", title:str="", parent:str="", prev:str="",
                 _next:str="", first:str="", last:str="", count:int=0,
                 dest:str="", depth:int=0, start:int=0, end:int=0):
        self.id = _id
        self.id = self.id.replace("obj", "R")
        self.title = title
        self.parent = parent
        self.prev = prev
        self.next = _next
        self.first = first
        self.last = last
        self.count = count
        self.dest = dest
        self.depth = depth
        self.start = start
        self.end = end

    def parse_from_raw(raw:str):
        # First, grab the ID from the first line.
        _id = raw[:raw.index("\n")]

        # Now, look for the optional properties
        title = ""
        parent = ""
        prev = ""
        _next = ""
        first = ""
        last = ""
        count = 0
        dest = ""

        # Parse title
        if "/Title" in raw:
            title = raw[raw.index("/Title(")+7:]
            title = title[:title.index("/")-1]
            title = title.replace("\\(", "(")
            title = title.replace("\\)", ")")

        # Parse parent
        if "/Parent" in raw:
            parent = raw[raw.index("/Parent")+7:].strip()
            parent = parent[:parent.index("/")]

        # Parse prev
        if "/Prev" in raw:
            prev = raw[raw.index("/Prev")+5:].strip()
            prev = prev[:prev.index("/")]

        # Parse next
        if "/Next" in raw:
            _next = raw[raw.index("/Next")+5:].strip()
            _next = _next[:_next.index("/")]

        # Parse first
        if "/First" in raw:
            first = raw[raw.index("/First")+6:].strip()
            first = first[:first.index("/")]

        # Parse last
        if "/Last" in raw:
            last = raw[raw.index("/Last")+5:].strip()
            last = last[:last.index("/")]

        # Parse count
        if "/Count" in raw:
            temp = raw[raw.index("/Count")+6:].strip()
            if "/" in temp:
                temp = temp[:temp.index("/")]
            else:
                temp = temp[:temp.index(">")]
            count = int(temp)

        # Parse dest
        if "/Dest" in raw:
            dest = raw[raw.index("/Dest[")+6:].strip()
            dest = dest[:dest.index("/")]


        # Return a newly created outline element
        return OutlineElement(_id=_id, title=title, parent=parent, prev=prev,
                              _next=_next, first=first, last=last, count=count,
                              dest=dest)

    def __str__(self):
        spaces = " "*self.depth
        return f"{spaces}{self.title} - {self.dest}"

class Node():
    def __init__(self, data:OutlineElement, children:list):
        self.data = data
        self.children = children

def build_tree(root:OutlineElement, depth=0):
    global outline_elements

    children = list()
    if root.count != 0:
        curr = outline_elements[root.first]
        while curr.id != outline_elements[root.last].id:
            children += [build_tree(curr, depth=depth+1)]
            curr = outline_elements[curr.next]
        children += [build_tree(curr, depth=depth+1)]
    root.depth = depth
    return Node(root, children)

def depth_first_list(root:Node, l:list):
    if len(root.children) != 0:
        l += [root.data]
        for child in root.children:
            depth_first_list(child, l)
    else:
        l += [root.data]
    return l

def insert_into_database(element:OutlineElement):
    # Return if the start page is in the ToC
    if element.start < 21:
        return

    # Generate the SQL expression
    sql = "INSERT INTO Article (title, start_page, end_page) VALUES (?, ?, ?)"
    cur.execute(sql, (element.title, element.start, element.end))

# First, open up the map file.
text = ""
with open("Projects/C# Documentation Scraper/map.txt", "r") as f:
    text = f.read().strip()

# Go through each line and make a mapping.
page_mapping = dict()
pages_in_order = list()
i = 1
for line in text.split("\n"):
    page_mapping[line] = i
    pages_in_order += [line]
    i += 1

# Go through the lines of the actual PDF and make a dictionary of
# outline elements. Stop when the object with ID 1160 is reached.
outline_elements = dict()
with codecs.open("Projects/C# Documentation Scraper/C# Documentation.pdf", "r",
                 encoding="utf-8", errors="ignore") as f:
    raw_text = f.read().strip()
    raw_text = raw_text[raw_text.index("2"):]
    for raw_obj in raw_text.split("\nendobj\n"):
        if "1160" in raw_obj:
            break
        elem = OutlineElement.parse_from_raw(raw_obj)
        outline_elements[elem.id] = elem

# Build the tree
tree = build_tree(outline_elements["1 0 R"])

# Turn the tree into a list
l = list()
depth_first_list(tree, l)

# Any page after ID 1159 is a filler page
for n in l:
    if n.dest != "":
        start_page = page_mapping[n.dest]

        curr = start_page+1
        r = int(pages_in_order[curr-1].split(" ")[0])
        while r > 1160 and curr < 1929:
            curr += 1
            r = int(pages_in_order[curr-1].split(" ")[0])
        end_page = curr-1

        n.start = start_page
        n.end = end_page

        # print(n, n.start, n.end)

        insert_into_database(n)

conn.commit()