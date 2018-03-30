var analytics = {
    at: {
        generateName: function(parts) {
            parts = parts || [];
            var tmp = [];

            for(var i = 0; i < parts.length; i++) {
                if (parts[i] && parts[i].toLowerCase() !== 'none') tmp.push(parts[i]);
            }

            return tmp.join('::');
        },
        initialize: function(parts, lang, zone) {
            var pageName = analytics.at.generateName(parts);

            if (pageName === "" || pageName === "default") {
                pageName = "Homepage";
            }

            window.ATInternet = {
                onTrackerLoad: function() {
                    window.tag = new window.ATInternet.Tracker.Tag();

                    if (!!sessionStorage.getItem("algolia-search")) {
                        var search = JSON.parse(sessionStorage.getItem("algolia-search"));
                        sessionStorage.removeItem('algolia-search');
                        tag.internalSearch.set(search);
                    }

                    if (sessionStorage.getItem("user") != null) {
                        var getNIC = sessionStorage.getItem("user");
                        tag.identifiedVisitor.unset();
                        tag.identifiedVisitor.set({
                            id: getNIC
                        });
                    }
                    
                    tag.page.set({
                        name: pageName
                    });

                    tag.customVars.set({
                        site: {
                            1: "[" + lang + "]",
                            2: "[" + zone + "]"
                        }
                    });

                    tag.dispatch();
                }
            };
            (function() {
                var at = document.createElement("script");
                at.type = "text/javascript";
                at.async = true;
                at.src = "https://www.ovh.com/fr/js/analytics/smarttag-docs.js";
                (document.getElementsByTagName("head")[0] || document.getElementsByTagName("body")[0] || document.getElementsByTagName("script")[0].parentNode).insertBefore(at, null)
            })()
        }
    }
};
