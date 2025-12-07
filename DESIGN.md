# MUSE

## Where to run Muse

The project was implemented in cs50 and can be run there with flask run. It was not pushed on a server, or implemented anywhere else. I have tried to use my own VS code to run it, but some of the CS50 tools I have used here requires a module called distutils that seems to have deprecated. In fear of not being able to have it run for you on time, I am leaving everything as is, and it is best to use CS50 codespace and 'flask run' there.


## Testing with existing records

Here are my credentials, if you would like to test with some populated fields:

username: adrien
password: harvard


## Design and implementation Choices

### Good outcome
[x] Users can register, login, logout.

[x] Users can click on a button which will redirect to another page and generate a random piece of art from the MET collection. A timer starts. * The timer was not implemented unfortunately *

[x] Users can answer some questions on a different page, "like" the art, and jot down thoughts on the art piece you observed, creating a record in the database.

[x] you can access these records on a different page, both as a table and as individual record.

[x] The application styling is polished and responsive. It works as well on a phone than it does on a desktop. * Although it is responsive, it is not as polished as I would like it to be. It is VERY basic and I heavily use Bootstrap *

[x] CSS and HTML passes the markup validator without error.

### Better outcome

[x] The API calls are efficient. The data is cached to avoid too many calls.

[x] Pagination is added, making navigation easier. * Implemented on the departments search page *

[x] Users can select a specific artist, period, or type of art that will be generated. For example "Vincent van Gogh," "Claude Monet" or "Painting," "Photograph" or "Egyptian art" etc.

[x] Users can access a page which provide useful information, such as their longest observed piece of art, or which artist you have liked the most, and more.

[x] HTML and CSS is improved for accessibility.

### Best outcome

[x] Users can filter tables for granular search of their previous records. * This is implemented only once, in the Stats page, with the artist most reflected on, which displays only the record filtered for that artist *

[ ] Users can change their preferences of artists, periods etc from the profile page. * This became irrelevant *

[x] Users can select arts coming from specific departments.

[ ] Users can create lists in which you can select MULTIPLE artists, periods, or type of art that will be generated. Users can then have different categories, which you can pick to generate a specific selection. * The unfiltered response made it inefficient *


## Page by Page

### Login, Logout, Profile, Register, Apology

These 4 routes were recycled from cs50 Finance PSet. If I have changed anything, it is not worth mentioning here.

### Art Surprise

Art surprise is the core feature of the website. The idea was to be randomly select an object from a Museum collection and display it in HD for the user to enjoy. I had found the MET museum API, which was free and did not require any authentication. Their documentation was simple, and offered the feature I was looking for. But one issue arose quickly. The API would not return a filtered query, but instead return the entire list of objects (or close) no matter what. Finding a painting which has a public access and a link in the object became extremely random, and all the validation is made in the back end instead. Nonetheless, I was able to drastically reduce the amount of artwork I'd display that did not fit my requirements (Has an image, is a painting etc).

It works for this project, but to take this further, I would use a different API.

Currently, this is how random_art works:

I fetch the list of object from the MET museum that *supposedly* fit my requirements, and I cache the list as to not call again.

I then randomly select an ID from that list, check that it does fit the requirement. If it does, I display it, if not, I select a different random ID. As a courtesy, I limit the amount of random check to 25 (as a constant) which seems to be more than enough. I had noticed that roughly 1/7 object did not fit one of the requirements.

### Details

The Art surprise page is part of a component that I reuse in the details page which is displayed if a user select to "view" an artwork already seen before. I use OpenSeaDragon as a tile viewer which allows for displaying the artwork in HD and gives more functionality, such as zoom in and out, going full screen etc. OpenSeaDragon is Javascript and can be found in the muse.js.

### My Reflections

My reflections page is the interface for a database query, which display all the records a user has created by "writing their impressions." I leverage the HTML/CSS by having a thumbnail image containing an anchor tag with the full size of the image.

#### View

From this page, it is also possible to view the artwork, which will pass in the MET ID of the Artwork into a similar page used for the Random_art, leveraging Components (templates/components/art_info.html).

#### Edit

It is also possible to Edit the reflection, which will redirect to the Reflection.html page, get the existing for that record ID, and display them on the page for the user to edit if they wish so. Saving the new record will update the Database.

#### Delete

Deleting the reflection is also an option, which simply deletes the record from the database.

#### Like/Unlike

I have implemented a like/unlike function with Javascript, which I reuse on the "My Favorites" page. It is responsive, and does not refresh the page, but does a POST request to the back end, which sends a status back that I then use to change the inner html of the button from like to unlike.

### My Favorites

This page is the interface of another database query. If favorite is equal to 1 (true), then display it. The Like/Unlike functionality is also present on this page. The user can access the individual information for each artwork and preview the artwork on a different window, like in the "My Reflections" page.

### Departments and Global search

This route grew organically. I had started with the global search function and added the department later. Finally, the pagination came last and was quite intricate to implement. I have left a lengthy note in the code explaining the issues I encountered with the API filtering. Although the search works great and returns the correct artwork requested, I have to jump through some hoops for it by checking each individual object. This makes the process inefficient and so I have decided to lock the amount of record to display on the screen, as a courtesy to the MET.

For the department search, select one of the department ID in the select field. I then query for the list of object that are within that department and returns the entire list (without too many constraints). It is frequent to not have a picture in the response.

For the global search, I use the MET endpoint for a global search, although this time I pass it through the get_art function, which will only return the art if it has an image url, and is of type painting. This is only for this project, as MANY objects do not have a url.

In both search, I display the result with a 5 records pagination, in the gallery.html file.

### Stats

The stats page returns 4 different queries from the database.

#### Favorite artist

Returns the artist that appears the most in favorite (where favorite = 1). The button in that same card is an action for a search for more artwork from that same artist.

#### Artist most reflected on

Returns the artist that has the most artwork reflected on in the User's db. The button in that same card redirect to the 'my reflections' page but only display the record which contains the artist name as artistName. This is an extension, yet different route, of the history function which returns ALL artworks.

#### Total liked paintings

The total amount of records with favorite = 1 for the registered user.

#### Total amount of reflections

The total amount of reflections for the registered user.


## What didn't work

### Issues during implementations

Some issues arose during implementation, the first one being the data itself returned by the API. Unfortunately, there is very little to no filtering done at the source, and everything must be done on my side. This made the calls very inefficient, with subsequent loading times. Some features were therefore not interesting anymore to implement, although it was technically possible. An example would be to create categories, in which the users would be able to select or input specific parameters that can then be searched (artist, period, etc). As it stands, the response would return ALL object IDs, and I have to check each object if they satisfy the parameters. The inefficiency of it all is observable in the departments search function and in the global search function, which can take 4/5 seconds to load, with very little constrains. This is also the reason why I am limiting the number of record I display with the search, as I would have to make another call for each object, search that the parameter is indeed what I am looking for, and move on to the next etc.


I heavily relied on Bootstrap's design for responsiveness. The design of Muse is very basic, as I have very little experience in web design. However, I have invested time to make sure the website is accessible, responsive and passes CSS and HTML validators.

### List and categories

The idea was to offer a way for the user to create list or categories. With specific parameters such as artist name, period, department, object name, to only offer random art satisfying those results. This was not possible with the MET endpoints. Their filter which didn't seem to work, forced back end validation at every level and would have made the list feature quite inefficient.


### Why does it take so long for the response?

The MET's response contains a list of over 700k objects which, despite the filtering done in the url, does not filter at all. Each object then need to be checked against the parameters that we're looking for. For example in art surprise, what we want to see is a painting. While the url explicitly filters for search?q="painting"&hasImages=true', the response does not filter and return the complete list.

Once the list is received, I then have to check each object and return only those that fulfill those parameters. While I cache the response and do not need to get the same list again and again, I still have to open a random amount of object to check.

As a courtesy to the MET, I limit the number of attempts.

### Having a timer was a great idea, why not implementing it?

I ran out of time, and this was not as easy as I thought this was going to be. My mistake was to think I could implement toward the end of the project. Unfortunately, by then, my routes were already less flexible, and I had a hard time figuring out how I can pass in the time spent on a painting into a different page, then save it into the database with the rest of the reflection. I got close, but I started to relay too much on AI (with only a couple of days left before the deadline, panic set in) and did not enjoy the process. I decided to stop.

#### Why not add the pagination on my reflections and my favorites?

For the same reason as above. I added more features that were not in my original proposal, such as my favorites, or the like/unlike function, which took a lot of time on their own. I, however, added pagination in the search function, in the gallery.html page.

### muse.db Diagram:


erDiagram

    USERS ||--|{ HISTORY

Available in schema.sql

With more time, I would have added another level to the database to keep track of favorite artworks. As it stands now, the user is not really favoriting a piece of art, but a record in history, meaning a painting could be liked twiced.

A table 'artwork' could be used to keep track of history and like at an individual level.

USERS ||--|{ HISTORY
ARTWORK ||--|{ HISTORY
ARTWORK ||--|{ LIKE



### Acknowledgments


The artwork data is coming from the MET museum Art collection Api available here: https://metmuseum.github.io/
The artwork viewer is OpenSeaDragon: https://openseadragon.github.io/



###

I have had a lot of fun designing this website. It is likely that I will take it further, as I had even more fun scrolling through the artwork and found myself just watching some of those breathtaking masterpiece.

If you play around with the website (not just the code), I hope you enjoy it just as much as I did.

