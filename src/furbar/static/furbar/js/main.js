(function ($) {
    "use strict";

    /*--
		Header Sticky
    -----------------------------------*/
    $(window).on('scroll', function(event) {    
        var scroll = $(window).scrollTop();
        if (scroll <= 1) {
            
            $(".header-sticky").removeClass("sticky");
        } else{
            $(".header-sticky").addClass("sticky");
        }
	});

    
    
    $(document).ready(function() {
        // Edit comment
        $('.edit-comment').on('click', function(e) {
            e.preventDefault();
            var commentId = $(this).data('comment-id');
            var commentText = $('#comment-text-' + commentId).text();
            $('#edit-comment-id').val(commentId);
            $('#edit-comment-text').val(commentText);
            $('#editCommentModal').modal('show');
        });
    
        $('#save-comment').on('click', function() {
            var formData = new FormData($('#edit-comment-form')[0]);
            var commentId = $('#edit-comment-id').val();
            var url = $('#edit-comment').attr('href');
            console.log(url);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                success: function(response) {
                    console.log(response);
                    $('#comment-text-' + commentId).text(response.text);
                    
                    
                    $('#editCommentModal').modal('hide');
                },
                error: function(response) {
                    console.error(response);
                }
            });
        });
    
        // Delete comment
        $('.delete-comment').on('click', function(e) {
            e.preventDefault();
            var commentId = $(this).data('comment-id');
            var url = $('#del-comment').attr('href');
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'comment_id': commentId
                    
                },

                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                success: function(response) {
                    console.log(response);
                    $('#single-reviews-' + commentId).remove();
                },
                error: function(response) {
                    console.error(response);
                }
            });
        });
    });
    
    $(document).ready(function() {
        console.log('main.js загружен и выполняется');
    
        function updateBasketCount(increment, targetElement) {
            var $basketCount = $(targetElement);
            var count = parseInt($basketCount.text()); // Преобразуем текст в число с основанием 10
                    
            count = count + increment;
            $basketCount.text(count >= 0 ? count : 0); // Убеждаемся, что счетчик не станет отрицательным
        }
    
        // Настройка получения CSRF токена для AJAX запросов
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
    
        function csrfSafeMethod(method) {
            // Эти методы HTTP не требуют защиты CSRF
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
    
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    
        var selectedRating = 0;
    
        // Обработка кликов по звездам
        $('#rating .star').on('click', function() {
            selectedRating = $(this).data('value');
            $('#rating .star').each(function() {
                if ($(this).data('value') <= selectedRating) {
                    $(this).find('i').removeClass('fa-star-o').addClass('fa-star');
                } else {
                    $(this).find('i').removeClass('fa-star').addClass('fa-star-o');
                }
            });
        });
    
        // Отправка формы через AJAX
        $(document).ready(function() {
            console.log('main.js загружен и выполняется');
        
            $('#review-images').on('change', function() {
                var $fileInput = $(this);
                var files = $fileInput[0].files;
        
                if (files.length > 0) {
                    var $newInput = $('<input type="file" name="images[]" multiple>');
        
                    $newInput.on('change', function() {
                        $('#review-images').trigger('change');
                    });
        
                    $fileInput.parent().append($newInput);
                }
            });
        
            function updateBasketCount(increment, targetElement) {
                var $basketCount = $(targetElement);
                var count = parseInt($basketCount.text());
        
                count = count + increment;
                $basketCount.text(count >= 0 ? count : 0);
            }
        
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');
        
            function csrfSafeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
        
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
        
            var selectedRating = 0;
        
            $('#rating .star').on('click', function() {
                selectedRating = $(this).data('value');
                $('#rating .star').each(function() {
                    if ($(this).data('value') <= selectedRating) {
                        $(this).find('i').removeClass('fa-star-o').addClass('fa-star');
                    } else {
                        $(this).find('i').removeClass('fa-star').addClass('fa-star-o');
                    }
                });
            });
        
            $('#review-form').on('submit', function(event) {
                event.preventDefault();
        
                var formData = new FormData(this);
                formData.append('vote', selectedRating);
        
                var additionalPath = $('#add-comment').attr('href');
                var model = $('#add-comment').attr('model');
                var objId = $('#add-comment').attr('obj_id');
        
                formData.append('model', model);
                formData.append('obj_id', objId);
        
                $('input[type="file"]').not(':first').remove();
                $.ajax({
                    url: additionalPath,
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    xhrFields: {
                        withCredentials: true
                    },
                    success: function(response) {
                        var newComment = `
        <div id="single-reviews-${response.comment_id}" class="single-reviews">
            <div class="comment-author">
                <a href="${response.username_image}">
                    <img src="${response.username_image}" alt="UserImage">
                </a>
            </div>
            <div class="comment-content">
                <div class="author-name-rating">
                    <h6 class="name">${response.username}</h6>
                    <div class="review-star">
                        <div class="star" style="width: ${response.vote}%;"></div>
                    </div>
                </div>
                <span class="date">${response.date}</span>
                <p id="comment-text-${response.comment_id}">${response.text}</p>`;
        
                        response.images_url.forEach(function(image) {
                            newComment += `
                <a href="${image.large_url}">
                    <img src="${image.preview_url}" alt="CommentImage" style="border-radius: 5px;">
                </a>`;
                        });
        
                        newComment += `
                <p></p>
                <p></p>
                <div class="comment-actions">
                    <a href="#" class="edit-comment" data-comment-id="${response.comment_id}"><i class="fa fa-edit"></i></a>
                    <a href="#" class="delete-comment" data-comment-id="${response.comment_id}"><i class="fa fa-trash"></i></a>
                </div>
            </div>
        </div>`;
        
                        console.log(newComment);
                        $('.commentss').append(newComment);
                        $('#review-form')[0].reset();
                        selectedRating = 0;
                        $('#rating .star i').removeClass('fa-star').addClass('fa-star-o');
                    }
                });
            });
        
            // Edit comment with event delegation
            $('.commentss').on('click', '.edit-comment', function(e) {
                e.preventDefault();
                var commentId = $(this).data('comment-id');
                var commentText = $('#comment-text-' + commentId).text();
                $('#edit-comment-id').val(commentId);
                $('#edit-comment-text').val(commentText);
                $('#editCommentModal').modal('show');
            });
        
            $('#save-comment').on('click', function() {
                var formData = new FormData($('#edit-comment-form')[0]);
                var commentId = $('#edit-comment-id').val();
                var url = $('#edit-comment').attr('href');
                console.log(url);
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        console.log(response);
                        $('#comment-text-' + commentId).text(response.text);
                        $('#editCommentModal').modal('hide');
                    },
                    error: function(response) {
                        console.error(response);
                    }
                });
            });
        
            // Delete comment with event delegation
            $('.commentss').on('click', '.delete-comment', function(e) {
                e.preventDefault();
                var commentId = $(this).data('comment-id');
                var url = $('#del-comment').attr('href');
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'comment_id': commentId
                    },
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        console.log(response);
                        $('#single-reviews-' + commentId).remove();
                    },
                    error: function(response) {
                        console.error(response);
                    }
                });
            });
        });
        
        
        
    
        // Делегирование событий для элементов с классом bask
        $(document).on('click', '.bask', function(event) {
            event.preventDefault(); // предотвращает переход по ссылке
            var $this = $(this);
            var url;
        
            if ($this.hasClass('active')) {
                url = $this.data('delete-url'); // URL для удаления
            } else {
                url = $this.data('add-url'); // URL для добавления
            }
        
            $.ajax({
                url: url,
                type: 'GET', // или 'POST' в зависимости от вашего представления
                xhrFields: {
                    withCredentials: true // включает отправку куки с запросом
                },
                success: function(response) {
                    // Обработка успешного ответа
                    if ($this.hasClass('active')) {
                        $this.removeClass('active');
                        $this.css('background-color', '');
                        $this.text('Добавить в корзину');
                        updateBasketCount(-1, '.firstBasket');
                        updateBasketCount(-1, '.secondBasket');
                    } else {
                        $this.addClass('active');
                        $this.css('background-color', 'orange');
                        $this.text('Убрать из корзины');
                        updateBasketCount(1, '.firstBasket');
                        updateBasketCount(1, '.secondBasket');
                    }
                },
                error: function(xhr, status, error) {
                    // Обработка ошибки
                    alert('Ошибка при добавлении/удалении товара из корзины');
                }
            });
        });
    
        // Делегирование событий для элементов с классом add-to-basket
        $(document).on('click', '.add-to-basket', function(event) {
            event.preventDefault(); // предотвращает переход по ссылке
            var $this = $(this);
            var url;
    
            if ($this.hasClass('active')) {
                url = $this.data('delete-url'); // URL для удаления
            } else {
                url = $this.data('add-url'); // URL для добавления
            }
    
            $.ajax({
                url: url,
                type: 'GET', // или 'POST' в зависимости от вашего представления
                xhrFields: {
                    withCredentials: true // включает отправку куки с запросом
                },
                success: function(response) {
                    // Обработка успешного ответа
                    if ($this.hasClass('active')) {
                        $this.removeClass('active');
                        $this.css('background-color', '');
                        updateBasketCount(-1, '.firstBasket');
                        updateBasketCount(-1, '.secondBasket');
                    } else {
                        $this.addClass('active');
                        $this.css('background-color', 'orange');
                        updateBasketCount(1, '.firstBasket');
                        updateBasketCount(1, '.secondBasket');
                    }
                },
                error: function(xhr, status, error) {
                    // Обработка ошибки
                    alert('Ошибка при добавлении/удалении товара из корзины');
                }
            });
        });
    
        // Делегирование событий для элементов с классом add-to-wishlist
        $(document).on('click', '.add-to-wishlist', function(event) {
            event.preventDefault(); // предотвращает переход по ссылке
            var $this = $(this);
            var url;
    
            if ($this.hasClass('active')) {
                url = $this.data('delete-url'); // URL для удаления
            } else {
                url = $this.data('add-url'); // URL для добавления
            }
    
            $.ajax({
                url: url,
                type: 'GET', // или 'POST'
                xhrFields: {
                    withCredentials: true // включает отправку куки с запросом
                },
                success: function(response) {
                    // Обработка успешного ответа
                    if ($this.hasClass('active')) {
                        $this.removeClass('active');
                        $this.css('background-color', '');
                    } else {
                        $this.addClass('active');
                        $this.css('background-color', 'orange');
                    }
                },
                error: function(xhr, status, error) {
                    // Обработка ошибки
                    alert('Ошибка при добавлении/удалении товара из избранного');
                }
            });
        });
    });
    
    
    /*--
		Menu Active
    -----------------------------------*/
    $(function () {
    var url = window.location.pathname; 
    var activePage = url.substring(url.lastIndexOf('/') + 1); 
        $('.nav-menu li a').each(function () { 
            var linkPage = this.href.substring(this.href.lastIndexOf('/') + 1); 
    
            if (activePage == linkPage) { 
                $(this).closest("li").addClass("active"); 
            }
        });
    })



    /*--
        Bootstrap dropdown
    -----------------------------------*/
    // Add slideDown animation to Bootstrap dropdown when expanding.
    $('.dropdown').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });

    // Add slideUp animation to Bootstrap dropdown when collapsing.
    $('.dropdown').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });


    /*--
        Off Canvas Menu
    -----------------------------------*/
	


  	$('.mobile-menu-open').on('click', function(){
        $('.off-canvas-box').addClass('open')
        $('.menu-overlay').addClass('open')
    });
    
    $('.menu-close').on('click', function(){
        $('.off-canvas-box').removeClass('open')
        $('.menu-overlay').removeClass('open')
    });
    
    $('.menu-overlay').on('click', function(){
        $('.off-canvas-box').removeClass('open')
        $('.menu-overlay').removeClass('open')
    });

    /*Variables*/
    var $offCanvasNav = $('.canvas-menu'),
    $offCanvasNavSubMenu = $offCanvasNav.find('.sub-menu, .mega-sub-menu, .menu-item ');

    /*Add Toggle Button With Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.parent().prepend('<span class="mobile-menu-expand"></span>');

    /*Close Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.slideUp();

    /*Category Sub Menu Toggle*/
    $offCanvasNav.on('click', 'li a, li .mobile-menu-expand, li .menu-title', function(e) {
        var $this = $(this);
        if (($this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/)) && ($this.attr('href') === '#' || $this.hasClass('mobile-menu-expand'))) {
            e.preventDefault();
            if ($this.siblings('ul:visible').length) {
                $this.parent('li').removeClass('active-expand');
                $this.siblings('ul').slideUp();
            } else {
                $this.parent('li').addClass('active-expand');
                $this.closest('li').siblings('li').find('ul:visible').slideUp();
                $this.closest('li').siblings('li').removeClass('active-expand');
                $this.siblings('ul').slideDown();
            }
        }
    });

    $( ".sub-menu, .mega-sub-menu, .menu-item" ).parent( "li" ).addClass( "menu-item-has-children" );
    $( ".mega-sub-menu" ).parent( "li" ).css( "position", "static" );


    /*--
        Slider
    -----------------------------------*/
    var slider = new Swiper('.slider-active .swiper-container', {
        speed: 600,
        effect: "fade",
        loop: false,
        pagination: {
            el: '.slider-active .swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.slider-active .swiper-button-next',
            prevEl: '.slider-active .swiper-button-prev',
        },
        // autoplay: {
        //     delay: 8000,
        // },
    }); 


    /*--
        Product
    -----------------------------------*/
    var product = new Swiper('.product-active .swiper-container', {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: false,
        navigation: {
            nextEl: '.product-active .swiper-button-next',
            prevEl: '.product-active .swiper-button-prev',
        },
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            }
        }
    });


    /*--
        Product 02
    -----------------------------------*/
    var product = new Swiper('.product-active-02 .swiper-container', {
        slidesPerView: 4,
        spaceBetween: 30,
        loop: false,
        navigation: {
            nextEl: '.product-active-02 .swiper-button-next',
            prevEl: '.product-active-02 .swiper-button-prev',
        },
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 4,
            }
        }
    });


    /*--
        products Banner
    -----------------------------------*/
    var product = new Swiper('.products-banner-active .swiper-container', {
        slidesPerView: 4,
        spaceBetween: 0,
        loop: false,        
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            },
            1200: {
                slidesPerView: 4,
            }
        }
    });


    /*--
        Blog
    -----------------------------------*/
    var product = new Swiper('.blog-active .swiper-container', {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: false,
        navigation: {
            nextEl: '.blog-active .swiper-button-next',
            prevEl: '.blog-active .swiper-button-prev',
        },
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            }
        }
    });


    /*--
        Testimonial
    -----------------------------------*/
    var slider = new Swiper('.testimonial-active .swiper-container', {
        speed: 600,
        loop: false,
        pagination: {
            el: '.testimonial-active .swiper-pagination',
            clickable: true,
        },
        // autoplay: {
        //     delay: 8000,
        // },
    }); 


    /*--
        Blog Gallery Active
    -----------------------------------*/
    var blog = new Swiper('.gallery-active .swiper-container', {
        slidesPerView: 1,
        spaceBetween: 0,
        loop: false,
        navigation: {
            nextEl: '.gallery-active .swiper-button-next',
            prevEl: '.gallery-active .swiper-button-prev',
        },        
    });


    /*--
        Countdown
    -----------------------------------*/
    function makeTimer($endDate, $this, $format) {
        var today = new Date();
        var BigDay = new Date($endDate),
          msPerDay = 24 * 60 * 60 * 1000,
          timeLeft = (BigDay.getTime() - today.getTime()),
          e_daysLeft = timeLeft / msPerDay,
          daysLeft = Math.floor(e_daysLeft),
          e_hrsLeft = (e_daysLeft - daysLeft) * 24,
          hrsLeft = Math.floor(e_hrsLeft),
          e_minsLeft = (e_hrsLeft - hrsLeft) * 60,
          minsLeft = Math.floor((e_hrsLeft - hrsLeft) * 60),
          e_secsLeft = (e_minsLeft - minsLeft) * 60,
          secsLeft = Math.floor((e_minsLeft - minsLeft) * 60);
    
        var yearsLeft = 0;
        var monthsLeft = 0
        var weeksLeft = 0;
    
        if ($format != 'short') {
          if (daysLeft > 365) {
            yearsLeft = Math.floor(daysLeft / 365);
            daysLeft = daysLeft % 365;
          }
    
          if (daysLeft > 30) {
            monthsLeft = Math.floor(daysLeft / 30);
            daysLeft = daysLeft % 30;
          }
          if (daysLeft > 7) {
            weeksLeft = Math.floor(daysLeft / 7);
            daysLeft = daysLeft % 7;
          }
        }
    
        var yearsLeft = yearsLeft < 10 ? "0" + yearsLeft : yearsLeft,
          monthsLeft = monthsLeft < 10 ? "0" + monthsLeft : monthsLeft,
          weeksLeft = weeksLeft < 10 ? "0" + weeksLeft : weeksLeft,
          daysLeft = daysLeft < 10 ? "0" + daysLeft : daysLeft,
          hrsLeft = hrsLeft < 10 ? "0" + hrsLeft : hrsLeft,
          minsLeft = minsLeft < 10 ? "0" + minsLeft : minsLeft,
          secsLeft = secsLeft < 10 ? "0" + secsLeft : secsLeft,
          yearsText = yearsLeft > 1 ? 'Years' : 'year',
          monthsText = monthsLeft > 1 ? 'Months' : 'month',
          weeksText = weeksLeft > 1 ? 'Weeks' : 'week',
          daysText = daysLeft > 1 ? 'Days' : 'day',
          hourText = hrsLeft > 1 ? 'Hours' : 'hr',
          minsText = minsLeft > 1 ? 'Mints' : 'min',
          secText = secsLeft > 1 ? 'Secs' : 'sec';
    
        var $markup = {
          wrapper: $this.find('.countdown__item'),
          year: $this.find('.yearsLeft'),
          month: $this.find('.monthsLeft'),
          week: $this.find('.weeksLeft'),
          day: $this.find('.daysLeft'),
          hour: $this.find('.hoursLeft'),
          minute: $this.find('.minsLeft'),
          second: $this.find('.secsLeft'),
          yearTxt: $this.find('.yearsText'),
          monthTxt: $this.find('.monthsText'),
          weekTxt: $this.find('.weeksText'),
          dayTxt: $this.find('.daysText'),
          hourTxt: $this.find('.hoursText'),
          minTxt: $this.find('.minsText'),
          secTxt: $this.find('.secsText')
        }
    
        var elNumber = $markup.wrapper.length;
        $this.addClass('item-' + elNumber);
        $($markup.year).html(yearsLeft);
        $($markup.yearTxt).html(yearsText);
        $($markup.month).html(monthsLeft);
        $($markup.monthTxt).html(monthsText);
        $($markup.week).html(weeksLeft);
        $($markup.weekTxt).html(weeksText);
        $($markup.day).html(daysLeft);
        $($markup.dayTxt).html(daysText);
        $($markup.hour).html(hrsLeft);
        $($markup.hourTxt).html(hourText);
        $($markup.minute).html(minsLeft);
        $($markup.minTxt).html(minsText);
        $($markup.second).html(secsLeft);
        $($markup.secTxt).html(secText);
    }
    
    $('.countdown').each(function () {
        var $this = $(this);
        var $endDate = $(this).data('countdown');
        var $format = $(this).data('format');
        setInterval(function () {
          makeTimer($endDate, $this, $format);
        }, 0);
    });


    /*--
		Back to top Script
	-----------------------------------*/
    // Show or hide the sticky footer button
    $(window).on('scroll', function (event) {
        if ($(this).scrollTop() > 600) {
            $('.back-to-top').fadeIn(200)
        } else {
            $('.back-to-top').fadeOut(200)
        }
    });

    //Animate the scroll to yop
    $('.back-to-top').on('click', function (event) {
    event.preventDefault();

        $('html, body').animate({
            scrollTop: 0,
        }, 1500);
    });


    /*--
        Nice Select Activation 
    -----------------------------------*/
    $('.nice_select').niceSelect();    


    /*--
        select2
    -----------------------------------*/
    $(".select2").select2({
        tags: true
    });


    /*--
        ionRangeSlider Activation 
    -----------------------------------*/
    $("#price-range").ionRangeSlider({
        type: "double",
        grid: false,
        min: 16,
        max: 500,
        from: 16,
        to: 300,
        prefix: "$",
    });


    /*--
        Product Details Zoom Activation
    -----------------------------------*/
    $('.zoom').zoom();


    /*--
        Product Details
    -----------------------------------*/
    var galleryThumbs = new Swiper('.details-gallery-thumbs .swiper-container', {
        spaceBetween: 20,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true,
        navigation: {
          nextEl: '.details-gallery-thumbs .swiper-button-next',
          prevEl: '.details-gallery-thumbs .swiper-button-prev',
        },
        breakpoints: {          
            0: {
                spaceBetween: 10,
                slidesPerView: 3,
            },
            576: {
                slidesPerView: 4,
            },
        }
      });
      var galleryTop = new Swiper('.details-gallery-images .swiper-container', {
        spaceBetween: 10,     
        thumbs: {
          swiper: galleryThumbs
        }
    });


    /*--
        Quick View
    -----------------------------------*/
    var galleryThumbs = new Swiper('.quick-gallery-thumbs .swiper-container', {
        spaceBetween: 20,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true,
        navigation: {
          nextEl: '.quick-gallery-thumbs .swiper-button-next',
          prevEl: '.quick-gallery-thumbs .swiper-button-prev',
        },
        breakpoints: {          
            0: {
                spaceBetween: 10,
                slidesPerView: 3,
            },
            576: {
                slidesPerView: 4,
            },
        }
      });
      var galleryTop = new Swiper('.quick-gallery-images .swiper-container', {
        spaceBetween: 10,     
        thumbs: {
          swiper: galleryThumbs
        }
    });


    /*--
        Product Quantity Activation
    -----------------------------------*/
    $('.add').on('click', function () {
        if ($(this).prev().val()) {
            $(this).prev().val(+$(this).prev().val() + 1);
        }
    });
    $('.sub').on('click', function () {
        if ($(this).next().val() > 1) {
            if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
        }
    });


    /*--
		Rating Script
	-----------------------------------*/

	$("#rating li").on('mouseover', function(){
		var onStar = parseInt($(this).data('value'), 10);
		var siblings = $(this).parent().children('li.star');
		Array.from(siblings, function(item){
			var value = item.dataset.value;
			var child = item.firstChild;
			if(value <= onStar){
				child.classList.add('hover')
			} else {
				child.classList.remove('hover')
			}
		})
	})

	$("#rating").on('mouseleave', function(){
		var child = $(this).find('li.star i');
		Array.from(child, function(item){
			item.classList.remove('hover');
		})
	})

	
	$('#rating li').on('click', function(e) {
		var onStar = parseInt($(this).data('value'), 10);
		var siblings = $(this).parent().children('li.star');
		Array.from(siblings, function(item){
			var value = item.dataset.value;
			var child = item.firstChild;
			if(value <= onStar){
				child.classList.remove('hover', 'fa-star-o');
				child.classList.add('fa-star')
			} else {
				child.classList.remove('fa-star');
				child.classList.add('fa-star-o')
			}
		})
	}) 


    /*--
        Odometer Activation 
    -----------------------------------*/
    if( $('.odometer').length ){

		var elemOffset = $('.odometer').offset().top;
		var winHeight = $(window).height();
		if(elemOffset < winHeight){
			$('.odometer').each(function(){
				$(this).html($(this).data('count-to'));
			});
		}
		$(window).on('scroll', function(){
			var elemOffset = $('.odometer').offset().top;
			function winScrollPosition() {
				var scrollPos = $(window).scrollTop(),
					winHeight = $(window).height();
				var scrollPosition = Math.round(scrollPos + (winHeight / 1.2));
				return scrollPosition;
			}
			if ( elemOffset < winScrollPosition()) {
				$('.odometer').each(function(){
					$(this).html($(this).data('count-to'));
				});
			}	
		});
    };


    /*--
        Checkout Account Active
    -----------------------------------*/
    $('#account').on('click', function () {
        if ($('#account:checked').length > 0) {
          $('.checkout-account').slideDown();
        } else {
          $('.checkout-account').slideUp();
        }
    });
      
  
    /*--
        Checkout Shipping Active
    -----------------------------------*/
    $('#shipping').on('click', function () {
        if ($('#shipping:checked').length > 0) {
          $('.checkout-shipping').slideDown();
        } else {
          $('.checkout-shipping').slideUp();
        }
    });
      
  
    /*--
        Checkout Payment Active
    -----------------------------------*/
    var checked = $('.payment-radio input:checked')
    if (checked) {
        $(checked).siblings('.payment-details').slideDown(500);
    };
    $('.payment-radio input').on('change', function() {
        $('.payment-details').slideUp(500);
        $(this).siblings('.payment-details').slideToggle(500);
    });
  

    

    
})(jQuery);

