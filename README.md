# MUSE

#### Video Demo:

--
### Summary
--

Who does not take out their phone to scroll mindlessly when bored? Reflection is a web application that lets users select a random piece of art from the Met Museum collection to focus on the art rather than social media, and jot down their thoughts on the piece (author, period, etc). This project is inspired from the New York Times monthly art 10 minutes challenge (https://www.nytimes.com/spotlight/10-minute-challenge)

--
### Description
--

As a registered user, access the (almost) entire collection of paintings, coins, and other artefacts of the MET museum. The main feature of Muse is "Art Surprise." Instead of mindlessly scrolling through your phone, or doomscrolling the internet, randomly explore the MET's painting collection, discover new artwork, and enjoy unexpected momenent of exploration and reflection.

With Muse, save your mindful reflections, revisit your favorite artwork at your leisure, search for your favorite painter, sculptor, or era, or scrolls through the wonders of the MET's numerous departments and their artefacts.

--
### How to navigate Muse
--

## Register

A simple page, recycled from CS50 Pset Finance, on which the user can create a new record in the database as long as the username does not already exist.

## Login

A simple page, recycled from CS50 Pset Finance, on which the user can login.

## Art Surprise

The core functionality of Muse. Art Surprise randomly select one artwork from the vast collection of the MET museum. The artwork must fulfill some requirements: It must be of classification 'Painting' and contain a url of a photo of the artwork. While the classification is of type painting, it is normal to sometimes come accross "scroll" or "print," etc. The classification is not constrained to the "Object Name" which is much more precise.

The Art Surprise page contains a tile viewer which displays the Artwork in high resolution and offers the user the ability to zoom in and out, or go full screen, giving the ability to trully appreciate the art therein.

If the user decides to jot down their thoughts on the artwork, they can do so by clicking on "give your impression." This will lead them to the reflection page, on which the user can choose to write some of their thoughts (first impressions, connections, meaning, composition). Once saved, the artwork and some of its information (including its API ID) are saved in the database to be revisited in the Reflections page.

## My Reflections

My Reflections pages display all the user's artwork on which some thoughts were jotted down. The thumbnail can be selected which will open a new window with the large size picture. An action button contains three actions:

# View

The user access a detail page on which they can revisit the artwork in the HD viewer container, and give a new impression.

# Edit

The reflection can be edited if the user choose to do so. In edit mode, the current data in the database are displayed in the fields for the user to edit.

# Delete

The reflection can be deleted.

# Like/Unlike

Any art on this page can be liked or unliked, and can be found in "My favorites" page.

## My Favorites

My favorites page contains all the art that are liked by the user. Like in "My Reflections," the user can preview the artwork by clicking on the thumbnail, which will open a new window with a larger size image. By clicking the "view" button, the user will redirected to the Details Page, which renders the HD viewer container of the image along with some information.

On this page, the Art can be liked or unliked. An art that is unliked stays on the page until the page is refresh.

## Departments

From the Departments page, the user can select one of the MET's department and access the collection for that department. If the search is successful, the results will be displayed in a table on the gallery page. From the page therein, the user can preview the image by clicking on the thumbnail, which will open another window with a larger size image. The "view" button will lead them to the Details page on which the user can explore the art in the HD viewer container, and write their impressions if they choose to do so, therefore creating a record in the database.

## Stats

The Stats page offers 4 different insights, generated from query of the database:

# Favorite artist

Clicking on "See More" triggers a search of the MET's Collection, with the artist name as a search parameter.

# Artist most reflected on

Clicking on "Check my reflections" displays the filtered reflections for that artist only.

# Total liked paitings

# Total amount of reflections


## Search

Search has two routes:

# Departments

Discussed in the departments section.

# Global search:

The global search returns the list of objects that contains the query in their data, as per the MET api documentation. Searching for an artist name will not only returns the list of objects with that artist name, but objects that contains the query in other parts (title, constituents etc) which offers a broad range of choices for the user.

--
### Design and implementation Choices
--

## Good outcome
[x] Users can register, login, logout.
[x] Users can click on a button which will redirect to another page and generate a random piece of art from the MET collection. A timer starts. * The timer was not implemented unfortunately *
[x] Users can answer some questions on a different page, "like" the art, and jot down thoughts on the art piece they observed, creating a record in the database.
[x] The user can access these records on a different page, both as a table and as individual record.
[x] The application styling is polished and responsive. It works as well on a phone than it does on a desktop.
[x] CSS and HTML passes the markup validator without error.

## Better outcome

[x] The API calls are efficient. The data is cached to avoid too many calls.
[x] Pagination is added, making navigation easier. * Implemented on the departments search *
[x] Users can select a specific artist, period, or type of art that will be generated. For example "Vincent van Gogh," "Claude Monnet" or "Painting," "Photograph" or "Egyptian art" etc.
[x] Users can access a page which provide useful information, such as their longest observed piece of art, or which artist they have liked the most, and more.
[x] HTML and CSS is improved for accessibility.

## Best outcome

[x] Users can filter tables for granular search of their previous records. * This is implemented only once, in the Stats page, with the artist most reflected on, which displays only the record filtered for that artis *
[] Users can change their preferences of artists, periods etc from the profile page.
[x] Users can select arts coming from specific departments.
[] Users can create lists in which they can select MULTIPLE artists, periods, or type of art that will be generated. Users can then have different categories, which they can pick to generate a specific selection.


## Issues during implementations

Some issues arose during implementation, the first one being the data itself returned by the API. Unfortunately, there is very little to no filtering done at the source, and everything must be done on my side. This made the calls very inefficient, with subsequent loading times. Some features were therefore not interesting anymore to implement, although it was technically possible. An example would be to create categories, in wich the users would be able to select or input specific parameters that can then be searched (artist, period, etc). As it stands, the response would return ALL object IDs, and I have to check each object if they satisfy the parameters. The inneficinecy of it all is observable in the departments search function and in the global search function, which can take 4/5 seconds to load, with very little constrains. This is also the reason why I am limiting the number of record I display with the search, as I would have to make another call for each object, search that the parameter is indeed what I am looking for, and move on to the next etc.


I heavily relied on Bootstrap's design for responsiveness. The design of Muse is very basic, as I have very little experience in web design. However, I have invested time to make sure the website is accessible, responsive and passes CSS and HTML validators.


# Why does it take so long for the response?

The MET

--
### muse.db Diagram:
--

erDiagram

    USERS ||--|{ HISTORY

Available in schema.sql


--
## Acknowledgments
--

The artwork data is coming from the MET museum Art collection Api available here: https://metmuseum.github.io/
The artwork viewer is OpenSeaDragon: https://openseadragon.github.io/
