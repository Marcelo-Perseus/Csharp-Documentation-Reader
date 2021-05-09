"""
Information
-----------
Author: Marcelo Luciano
Organization: Perseus

Summary
-------
This script was used to parse out the master documentation PDF file
and input the parsed outline bounds into the local Article database.

Imports
-------
codecs
    Used to read the PDF without causing encoding errors.
sqlite3
    Used to interact with the local database.
"""

import codecs
import sqlite3

# Define a project folder to work in.
proj_folder = "Projects/Csharp-Documentation-Reader"

# Open up the database.
conn = sqlite3.connect(f"{proj_folder}/res/database.db")
cur = conn.cursor()

class OutlineElement():
    """
    A class to store information on an outline element in the master
    PDF outline.

    Attributes
    ----------
    id: str
        The PDF object ID of the element.
    title: str
        The title of the element.
    parent: str
        The PDF object ID of the element's parent.
    prev: str
        The PDF object ID of the previous element on the same depth.
    next: str
        The PDF object ID of the next element on the same depth.
    first: str
        The PDF object ID of the first child element.
    last: str
        The PDF object ID of the last child element.
    count: int
        The number of children of the element.
    dest: str
        The PDF object ID of the page destination for the element link.
    depth: int
        The element depth in the overall outline structure.
    start: int
        The start page of the element's linked article.
    end: int
        The last page of the element's linked article.

    Methods
    -------
    parse_from_raw(raw:str)
        Parses out an OutlineObject from the raw PDF text.
    __str__()
        Generates a string representation of the OutlineElement.
    """

    def __init__(self, _id:str="", title:str="", parent:str="", prev:str="",
                 _next:str="", first:str="", last:str="", count:int=0,
                 dest:str="", depth:int=0, start:int=0, end:int=0):
        """
        Creates an OutlineElement object with the given values

        Notes
        -----
        - All parameters are optional, but ones like the title and
        destination will appear in all of the generated objects.
        - At the start, the start and end variables will be 0. These
        are set later in the program when the values are discovered.

        Parameters
        ----------
        id: str, optional
            The PDF object ID of the element.
        title: str, optional
            The title of the element.
        parent: str, optional
            The PDF object ID of the element's parent.
        prev: str, optional
            The PDF object ID of the previous element on the same depth.
        next: str, optional
            The PDF object ID of the next element on the same depth.
        first: str, optional
            The PDF object ID of the first child element.
        last: str, optional
            The PDF object ID of the last child element.
        count: int, optional
            The number of children of the element.
        dest: str, optional
            The PDF object ID of the page destination for the element
            link.
        depth: int, optional
            The element depth in the overall outline structure.
        start: int, optional
            The start page of the element's linked article.
        end: int, optional
            The last page of the element's linked article.

        Returns
        -------
        Returns a new OutlineElement.
        """

        # Assign the object values.
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
        """
        Parses out an OutlineElement from the raw PDF text
        representation.

        Notes
        -----
        - The raw string will not have all of the parameters that an
        OutlineElement will take, but any that it finds will be included.

        Parameters
        ----------
        raw: str
            The raw string representation of the OutlineElement to
            create.

        Returns
        -------
        Returns a new OutlineElement from the given raw string.
        """

        # Grab the ID from the first line.
        # Note: This is given in the "obj" form as opposed to the "R"
        # form for the PDF object ID.
        _id = raw[:raw.index("\n")]

        # Create variables for the optional parameters.
        title = ""
        parent = ""
        prev = ""
        _next = ""
        first = ""
        last = ""
        count = 0
        dest = ""

        # Parse the title if possible.
        if "/Title" in raw:
            title = raw[raw.index("/Title(")+7:]
            title = title[:title.index("/")-1]
            title = title.replace("\\(", "(")
            title = title.replace("\\)", ")")

        # Parse the parent reference if possible.
        if "/Parent" in raw:
            parent = raw[raw.index("/Parent")+7:].strip()
            parent = parent[:parent.index("/")]

        # Parse the prev reference if possible.
        if "/Prev" in raw:
            prev = raw[raw.index("/Prev")+5:].strip()
            prev = prev[:prev.index("/")]

        # Parse the next reference if possible.
        if "/Next" in raw:
            _next = raw[raw.index("/Next")+5:].strip()
            _next = _next[:_next.index("/")]

        # Parse the first reference if possible.
        if "/First" in raw:
            first = raw[raw.index("/First")+6:].strip()
            first = first[:first.index("/")]

        # Parse the last reference if possible.
        if "/Last" in raw:
            last = raw[raw.index("/Last")+5:].strip()
            last = last[:last.index("/")]

        # Parse the count if possible.
        if "/Count" in raw:
            temp = raw[raw.index("/Count")+6:].strip()
            if "/" in temp:
                temp = temp[:temp.index("/")]
            else:
                temp = temp[:temp.index(">")]
            count = int(temp)

        # Parse the dest reference if possible.
        if "/Dest" in raw:
            dest = raw[raw.index("/Dest[")+6:].strip()
            dest = dest[:dest.index("/")]


        # Return a newly created OutlineElement.
        return OutlineElement(_id=_id, title=title, parent=parent, prev=prev,
                              _next=_next, first=first, last=last, count=count,
                              dest=dest)

    def __str__(self):
        """
        Creates and returns a string representation of the current
        OutlineElement object.

        Notes
        -----
        - The string is given as the title and the dest separated by
        a dash.

        Returns
        -------
        Returns a string representation of the current OutlineElement.
        """

        # Create and return the string.
        spaces = " "*self.depth
        return f"{spaces}{self.title} - {self.dest}"

class Node():
    """
    A tree node for sorting and reading the PDF outline.

    Notes
    -----
    - This node is slightly different from other trees in that the
    number of children is variable.
    - The children will be sorted by the order they appear in the PDF
    outline before being passed into a new object.

    Attributes
    ----------
    data: OutlineElement
        The data stored within the current node.
    children: list(Node)
        The list of children of the OutlineElement in data. The list
        is sorted by appearance order.
    """

    def __init__(self, data:OutlineElement, children:list):
        """
        Creates a new Node object.

        Parameters
        ----------
        data: OutlineElement
            The data stored within the current node.
        children: list(Node)
            The list of children of the OutlineElement in data. The list
            is sorted by appearance order.

        Returns
        -------
        Returns a new Node object with the given values.
        """

        # Assign the attributes.
        self.data = data
        self.children = children

def build_tree(root:OutlineElement, depth:int=0):
    """
    Recursively builds out a tree from the given root node.

    Notes
    -----
    - This function will recursively build out a tree representing
    the master PDF outline. I believe this is the way Adobe intended
    to read the outline information, so that's the way I did it.

    Parameters
    ----------
    root: OutlineElement
        The root OutlineElement for building the tree recursively.
    depth: int, optional
        The current depth within the recursive stack. Defaults to 0.

    Returns
    -------
    Returns a Node object representing the root of the newly created
    tree.
    """

    # Use the global outline_elements variable for accessing the
    # OutlineElements by ID.
    global outline_elements

    # Create a list for the children and loop through each child
    # making a new tree from each one. Then add the new tree to the
    # list of children to be passed to the return Node.
    children = list()
    if root.count != 0:
        curr = outline_elements[root.first]
        while curr.id != outline_elements[root.last].id:
            children += [build_tree(curr, depth=depth+1)]
            curr = outline_elements[curr.next]
        children += [build_tree(curr, depth=depth+1)]

    # Assign the depth to the root object.
    root.depth = depth

    # Return the new root node.
    return Node(root, children)

def depth_first_list(root:Node, l:list):
    """
    Generates a list from the given tree by looping through each
    element using a preorder depth-first traversal. (Root, Left, Right).
    This method does so recursively.

    Notes
    -----
    - This method doesn't return anything. Instead it will alter the
    given list when it adds more OutlineElement objects

    Parameters
    ----------
    root: Node
        The root to add to the list along with the children of the root.
    l: list(OutlineElement)
        The list to add the root and its children to.
    """

    # Add the root's data.
    l += [root.data]

    # If there are children, add them recursively.
    if len(root.children) != 0:
        for child in root.children:
            depth_first_list(child, l)


def insert_into_database(element:OutlineElement):
    """
    Inserts the given OutlineElement object into the local database.

    Notes
    -----
    - This method only adds the title, start page, and end page of the
    OutlineObject. The rest of the attributes for the object aren't
    stored.

    Parameters
    ----------
    element: OutlineElement
        The element to add to the database.
    """

    # Return if the start page is in the ToC.
    if element.start < 21:
        return

    # Generate the SQL expression and execute it.
    sql = "INSERT INTO Article (title, start_page, end_page) VALUES (?, ?, ?)"
    cur.execute(sql, (element.title, element.start, element.end))

# Open up the map file.
text = ""
with open(f"{proj_folder}/res/map.txt", "r") as f:
    text = f.read().strip()

# Go through each line and make a mapping dictionary.
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
with codecs.open(f"{proj_folder}/res/C# Documentation.pdf", "r",
                 encoding="utf-8", errors="ignore") as f:
    raw_text = f.read().strip()
    raw_text = raw_text[raw_text.index("2"):]
    for raw_obj in raw_text.split("\nendobj\n"):
        if "1160" in raw_obj:
            break
        elem = OutlineElement.parse_from_raw(raw_obj)
        outline_elements[elem.id] = elem

# Build the tree of the outline.
tree = build_tree(outline_elements["1 0 R"])

# Turn the tree into a sorted list.
l = list()
depth_first_list(tree, l)

# Determine the start and end pages of each article.
# Any page after ID 1159 is a filler page.
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

        # Add the new article to the database.
        insert_into_database(n)

# Commit changes to the database.
conn.commit()