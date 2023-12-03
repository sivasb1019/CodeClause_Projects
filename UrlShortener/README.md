# Django URL Shortener Project 🌐🔗

## Project Overview

- This Django-based URL Shortener is a web application designed to generate shortened versions of URLs provided by users.
- It's a simple yet efficient tool that creates shorter, more manageable links for lengthy URLs.
- Check out the demo video of the project [clcik here](https://www.linkedin.com/feed/update/urn:li:activity:7133410003222241280/).

## Features

- **Shortening URLs**: Converts long URLs into shorter, custom-generated links.
- **Redirection**: Redirects users from the shortened link to the original URL.
- **User Interface**: Provides a clean and user-friendly interface to input original URLs and obtain their shortened versions.


## Usage
- **Home Page**: Access the home page (`/`) to get started.
- **Create Shortened URL**: Enter the original URL in the provided form to generate a shortened link.
- **Redirection**: Use the shortened link to redirect to the original URL.

## Structure
- **`home.html`**: Home page HTML template.
- **`create.html`**: URL creation form HTML template.
- **`urlcreated.html`**: Template to display the created shortened URL.
- **`redirect.html`**: Template to redirect to the original URL.
- **`pagenotfound.html`**: Page for handling invalid or non-existing shortened URLs.

## Development Notes
- The project uses Django's ORM to manage ShortURL model instances.
- Random characters are generated for shortened URLs to ensure uniqueness.
- The application handles redirects and provides user-friendly interfaces for URL creation and redirection.

## Future Enhancements

- **User Authentication**: Implement user accounts to enable personalized URL management.
- **Analytics**: Track link clicks and provide statistics for shortened URLs.
- **Custom Shortened URLs**: Allow users to create custom short links.

## Contributing

Contributions to the project are welcome! Feel free to fork the repository, make changes, and submit a pull request.


 ## Project Demo
 
This project demo is posted on my [LinkedIn account](https://www.linkedin.com/feed/update/urn:li:activity:7133410003222241280/).
