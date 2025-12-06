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

## Search


--
### Design and implementation Choices
--


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
