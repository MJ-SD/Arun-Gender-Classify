console.log('smooth_scroll.js is loaded');
document.addEventListener('DOMContentLoaded', function () {
    // Add a small delay to ensure all elements are rendered
    setTimeout(function () {
        const homeButton = document.getElementById('home-button');
        const overallButton = document.getElementById('overall-button');
        const yearsButton = document.getElementById('years-button');
        const popularityButton = document.getElementById('popularity-button');
        const topAuthorsButton = document.getElementById('top-authors-button');
        const aboutButton = document.getElementById('about-button');
        if (homeButton) {
            homeButton.addEventListener('click', function () {
                console.log('Home button clicked');
                document.getElementById('home').scrollIntoView({ behavior: 'smooth' });
            });
        }

        if (overallButton) {
            overallButton.addEventListener('click', function () {
                console.log('Overall button clicked');
                document.getElementById('overall-gender').scrollIntoView({ behavior: 'smooth' });
            });
        }

        if (yearsButton) {
            yearsButton.addEventListener('click', function () {
                console.log('Years button clicked');
                document.getElementById('gender-years').scrollIntoView({ behavior: 'smooth' });
            });
        }

        if (popularityButton) {
            popularityButton.addEventListener('click', function () {
                console.log('Popularity button clicked');
                document.getElementById('popularity-gender').scrollIntoView({ behavior: 'smooth' });
            });
        }

        if (topAuthorsButton) {
            topAuthorsButton.addEventListener('click', function () {
                console.log('Top Authors button clicked');
                document.getElementById('top-authors').scrollIntoView({ behavior: 'smooth' });
            });
        }
        if (aboutButton) {
            aboutButton.addEventListener('click', function () {
                console.log('About button clicked');
                document.getElementById('about-cs').scrollIntoView({ behavior: 'smooth' });
            });
        }
    }, 500);  // Adding a 500ms delay to ensure everything is rendered
});
