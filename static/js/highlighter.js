$(document).ready(function() {
    $('#highlight-btn').click(function(event) {
        event.preventDefault();
        var mainText = $('#main-text').html();
        console.log('Main Text:', mainText);
        var keywordList = $('#keyword-list').val().split(',');
        console.log('Keyword List:', keywordList);
        $.each(keywordList, function(index, keyword) {
            var regex = new RegExp('\\b' + keyword.trim() + '\\b(?![^<]*>)', 'ig');
            mainText = mainText.replace(regex, '<span id="highlight-' + index + '" class="highlight">' + keyword.trim() + '</span>');
        });
        $('#main-text').html(mainText);
        return false;
    });


    $('#add-url-btn').click(function(event) {
        event.preventDefault();
        var url = $('#url').val();
        if (!url) {
            alert('Please enter a URL');
            return false;
        }
        $('span.highlight').each(function() {
            var keyword = $(this).text();
            $(this).wrap('<a href="' + url + '" title="' + url + '"></a>');
        });
    });
   
    $('#clear-btn').click(function(event) {
        event.preventDefault();
        $('span.highlight').removeClass('highlight');
    });
    
});
