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
        initialize: function(parts, code, name, cb) {
            var pageName = analytics.at.generateName(parts);

            if (pageName === '' || pageName === 'default') {
                pageName = 'Homepage';
            }

            window.tc_vars = {
                env_template : 'Website',
                page_name : pageName,
                env_country : '[' + code + ']',
                env_language : '[' + name + ']'
            }

            if (!!sessionStorage.getItem("algolia-search")) {
                var search = JSON.parse(sessionStorage.getItem("algolia-search"));
                window.tc_vars.searchKeywords = search.keyword;
                window.tc_vars.resultPosition = search.resultPosition;
            }

            if (!!sessionStorage.getItem("user")) {
                var nic = sessionStorage.getItem("user");
                window.tc_vars.user_code = nic;
            }

            if (cb && typeof cb === 'function') {
                cb();
            }
        }
    }
};
