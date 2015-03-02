function social(network, url, text){

    var socialNetworks = {
        facebook: {
            title: "Share on Facebook",
            cssclass: "social-facebook",
            shareurl: "https://www.facebook.com/sharer/sharer.php?u=" + url,
            height: 600,
            width: 600
        },
        twitter: {
            title: "Share on Twitter",
            cssclass: "social-twitter",
            shareurl: "https://twitter.com/intent/tweet?text=" + text + "&url=" + url,
            height: 600,
            width: 600
        },
        googleplus: {
            title: "Share on Google+",
            cssclass: "social-googleplus",
            shareurl: "https://plus.google.com/share?url=" + url,
            height: 600,
            width: 600
        }
    };


    var shareHeight = socialNetworks[network].height;
    var shareWidth = socialNetworks[network].width;
    var shareTop = ((screen.height/2) - (socialNetworks[network].height/2));
    var shareLeft = ((screen.width/2) - (socialNetworks[network].width/2))


    window.open(
        socialNetworks[network].shareurl, '',
        'menubar=no,toolbar=no,resizeable=no,scrollbars=no,height=' + shareHeight + ',width=' + shareWidth + ',top=' + shareTop + ',left=' + shareLeft
        );
 }