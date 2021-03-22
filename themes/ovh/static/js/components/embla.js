$(function() {
    const match = (bp) => {
        return window.matchMedia(bp).matches;
    };

    const detectSlidesToScroll = () => {
        if (match('(min-width: 1600px)')) return 4;
        if (match('(min-width: 1120px)')) return 3;
        if (match('(min-width: 768px)')) return 2;
        return 1;
    };

    const setupPrevNextButton = (prevBtn, nextBtn, embla) => {
        prevBtn.addEventListener('click', embla.scrollPrev, false);
        nextBtn.addEventListener('click', embla.scrollNext, false);
    };

    const disablePrevNextBtns = (prevBtn, nextBtn, embla) => {
        return () => {
            if (embla.canScrollPrev()) prevBtn.removeAttribute('disabled');
            else prevBtn.setAttribute('disabled', 'disabled');

            if (embla.canScrollNext()) nextBtn.removeAttribute('disabled');
            else nextBtn.setAttribute('disabled', 'disabled');
        };
    };

    const setupDotBtns = (dotsArray, embla) => {
        dotsArray.forEach((dotNode, i) => {
            dotNode.addEventListener('click', () => embla.scrollTo(i), false);
        });
    };

    const generateDotBtns = (dots, embla) => {
        const template = document.getElementById("embla-dot-template").innerHTML;
        dots.innerHTML = embla.scrollSnapList().reduce(acc => acc + template, "");
        return [].slice.call(dots.querySelectorAll(".embla__dot"));
    };

    const selectDotBtn = (dotsArray, embla) => () => {
        const previous = embla.previousScrollSnap();
        const selected = embla.selectedScrollSnap();
        dotsArray[previous].classList.remove("is-selected");
        dotsArray[selected].classList.add("is-selected");
    };

    const nb = detectSlidesToScroll();
    const options = { loop: false, slidesToScroll: nb, align: 'start' }

    const wrap = document.querySelector('.embla');
    const emblaNode = wrap.querySelector('.embla__viewport')
    const prevBtn = wrap.querySelector('.embla__button--prev');
    const nextBtn = wrap.querySelector('.embla__button--next');
    const dots = document.querySelector('.embla__dots');
    const embla = EmblaCarousel(emblaNode, options)

    const dotsArray = generateDotBtns(dots, embla);
    const setSelectedDotBtn = selectDotBtn(dotsArray, embla);
    const disablePrevAndNext = disablePrevNextBtns(prevBtn, nextBtn, embla);
    setupPrevNextButton(prevBtn, nextBtn, embla);
    setupDotBtns(dotsArray, embla);

    embla.on('resize', () => {
        const slidesToScroll = detectSlidesToScroll();
        embla.reInit({ slidesToScroll });
    });
    embla.on('select', setSelectedDotBtn);
    embla.on('select', disablePrevAndNext);
    embla.on('init', setSelectedDotBtn);
    embla.on('init', disablePrevAndNext);
});
