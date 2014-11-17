# -*- coding: utf-8 -*-


def create_page_header():
    """
    Returns the header of the webpage
    """
    html_container = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Radio gaga - Discover music played in your radio</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="Content-language" content="en">
    <link rel="stylesheet" href="css/template.css" type="text/css" />
    </head>
    """
    return(html_container)


def create_page_bottom():
    """
    Returns the bottom of the webpage
    """
    html_container = "</html>"
    return(html_container)


def create_page_footer():
    """
    Returns the footer of the page
    """
    html_container = """<div id="page">
    <div id="footer">Project Radio Gaga 2014 - All rights reserved.</div>
    </div>"""
    return(html_container)


def create_page_menu():
    """
    Returns the menu used for navigation
    """
    html_container = """<div id="page">
    <div id="top-banner">
    <div id="top-banner-logo">
    <a href="index.php">radiogaga</a>
    </div>
    <div id="top-banner-menu">
    <a href="mostplayed.php">most played</a>
    &nbsp &nbsp &nbsp &nbsp
    <a href="analysis.php">analysis</a>
    </div>
    </div>
    </div>
    """
    return(html_container)


def create_page_banner():
    """
    Returns the banner of the page
    """
    html_container = """
    <div class="artist-wall" style="background-image:
    url(cover/madonna.jpg)">
    <div class="artist-wall-overlay">
    <div id="intro">
    <p style="margin: 0px;">Welcome to Radio gaga.
    Discover music played in your radio.</p>
    </div>
    </div>
    </div>
    """
    return(html_container)


def create_page_content_mostplay():
    """
    Returns a div container showing a list of tracks
    """
    track_container = """
    <div id="track">
    <div id="track">
    <a href="artist/SamSmith/ImNotTheOnlyOne.php">
    <div id="album-img" style="background-image:
    url(images/cover-overlay100x100.png),
    url(cover/Im+Not+The+Only+One+Sam+Smith.jpg)">
    </div>
    </a>
    <span class="artist">
    <a href="artist/SamSmith/index.php">
    Sam Smith
    </a>
    </span>
    <br>
    <span class="track">
    <a href="artist/SamSmith/ImNotTheOnlyOne.php">
    Im Not The Only One
    </a></span>
    </div>
    </div>
    """
    return(track_container)


def create_page_index(path):
    """
    Saves the frontpage file defined in path ie 'index.php'
    """
    # Create the html container to save
    header = create_page_header()
    menu = create_page_menu()
    banner = create_page_banner()
    footer = create_page_footer()
    bottom = create_page_bottom()
    html_container = header + menu + banner + footer + bottom

    # Save to local file
    with open(path, 'w') as file_writer:
        file_writer.write(html_container)


create_page_index('C:/xampp/htdocs/test/index.php')
