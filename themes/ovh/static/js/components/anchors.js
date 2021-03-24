(() => {
    const getHeaders = () => {
        const selectors = [
            '#content h1',
            '#content h2',
            '#content h3',
            '#content h4',
            '#content h5',
            '#content h6',
        ];
        return document.querySelectorAll(selectors.join(','));
    };

    const slugify = (text, separator = "-") => {
        return text
            .toString()
            .normalize('NFD')                   // split an accented letter in the base letter and the acent
            .replace(/[\u0300-\u036f]/g, '')   // remove all previously split accents
            .toLowerCase()
            .trim()
            .replace(/[^a-z0-9 ]/g, '')   // remove all chars not letters, numbers and spaces (to be replaced)
            .replace(/\s+/g, separator);
    };

    const jump = (anchor) => {
        location.href = '#' + anchor;
    };

    const addUniqueId = (elements) => {
        const idList = elements.reduce((acc, current) => {
            if (current.id) {
                if (current.id in acc) {
                    acc[current.id]++;
                } else {
                    acc[current.id] = 0;
                }
            }
            return acc;
        }, {});

        elements
            .filter(elem => "" === elem.id)
            .forEach(elem => {
                let slug = slugify(elem.innerHTML);

                if (slug in idList) {
                    idList[slug]++;
                    slug += `-${idList[slug]}`;
                } else {
                    idList[slug] = 0;
                }

                elem.id = slug;
            });
    };

    const headers = Array.from(getHeaders().values());
    addUniqueId(headers);
    headers.forEach(elem => {
        elem.addEventListener('click', () => {
            jump(elem.id);
        });
    });
})()
