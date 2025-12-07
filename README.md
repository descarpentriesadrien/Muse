# MUSE

## Video Demo:  https://youtu.be/z2H-zJC4I1o

## Summary

Who does not take out their phone to scroll mindlessly when bored? Reflection is a web application that lets you select a random piece of art from the Met Museum collection to focus on the artwork rather than social media, and jot down your thoughts on the piece (impressions, composition etc). This project is inspired from the New York Times monthly 10 minutes challenge (https://www.nytimes.com/spotlight/10-minute-challenge)

## Description

As a registered user, access the (almost) entire collection of paintings, coins, and other artifacts of the MET museum. The main feature of Muse is "Art Surprise": Randomly explore the MET's painting collection, discover new artwork, and enjoy unexpected moment of exploration and reflection.

With Muse, save your mindful reflections, revisit your favorite artwork at your leisure, search for your favorite painter, sculptor, or era, and scroll through the wonders of the MET's numerous departments and their artifacts.

## How to navigate Muse
### Register

A page on which you can register.

### Login

A page on which you can login, using the credentials created on the register page.

### Art Surprise

The core functionality of Muse. By clicking on "Art Surprise," randomly access paintings from the vast collection of the MET museum.

The Art Surprise page contains a tile viewer which displays the Artwork in high resolution and functionality to zoom in and out, giving you the ability to truly appreciate the art therein.

If you decide to jot down your thoughts on the artwork, you can do so by clicking on "give your impression." This will lead you to the reflection page, on which you can choose to write some of your thoughts (first impressions, connections, meaning, composition). Once saved, the artwork and its information (including its MET ID) are saved in the database to be revisited in the Reflections page.

### My Reflections

My Reflections pages display all the artwork on which your thoughts were jotted down. The thumbnail can be selected which will open a new window with the large size picture. An action button contains three actions:

#### View

You can access a detail page on which you can revisit the artwork in the HD viewer container, and give a new impression.

#### Edit

The reflection can be edited if you choose to do so. In edit mode, the current data in the database are displayed in the fields for you to edit.

#### Delete

The reflection can be deleted.

#### Like/Unlike

Any art on this page can be liked or unliked, and can be found in "My favorites" page.

### My Favorites

My favorites page contains all the art that you "liked." Similar to "My Reflections," you can preview the artwork by clicking on the thumbnail, which will open a new window with a larger size image. By clicking the "view" button, you will be redirected to the Details Page, which renders the HD viewer container of the image along with some information.

On this page, the Art can be liked or unliked. An art that is unliked stays on the page until the page is refresh.

### Departments

From the Departments page, you can select one of the MET's department and access the collection for that department. If the search is successful, the results will be displayed in a table on the gallery page. From the page therein, you can preview the image by clicking on the thumbnail, which will open another window with a larger size image. The "view" button will lead you to the Details page on which you can explore the art in the HD viewer container, and write your impressions if you choose to do so, therefore creating a record in the database.

### Stats

The Stats page offers 4 different insights, generated from query of the database:

#### Favorite artist

The artist that appears the most in your favorites page. (If tied, it will display the first you have favorited)

Clicking on "See More" triggers a search of the MET's Collection, with the artist name as a search parameter.

#### Artist most reflected on

The artist that has the most painting you have come across and reflected on.

Clicking on "Check my reflections" displays the filtered reflections for that artist only.

#### Total liked paintings

The total amount of painting you have liked so far.

#### Total amount of reflections

The total amount of reflections you have written so far.

### Search

Search has two routes:

### Departments

Select one of the numerous departments at the MET museum and get access to their vast collection.

### Global search:

Search for any artist, title, object, departments. Any keyword that fits the search will return a list of object.
(For this project, to not appear broken from the lack of information in the Data response, I enforce a PrimaryImageUrl = True which limits the amount of response. Many of the artwork do not have a url, or are not publicly accessible.)


### Acknowledgments


The artwork data is coming from the MET museum Art collection Api available here: https://metmuseum.github.io/
The artwork viewer is OpenSeaDragon: https://openseadragon.github.io/

