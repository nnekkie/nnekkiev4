$(document).ready(function(){
    console.log('blog loaded');
    $('#blog-form').submit(function (e) {
        e.preventDefault();
    
        // CSRF token from the page
        const csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    
        // Form data
        let title = $('#blog-title').val();
        let fileInput = $('#blog-file')[0];
        var file = fileInput.files[0];
    
        // Log for debugging
        console.log(title);
        console.log(file ? file.name : 'No file selected');
    
        if (!title || !file) {
            alert('Title and file are required!');
            return;
        }
    
        // Prepare FormData
        var formData = new FormData();
        formData.append('blog-title', title);
        formData.append('blog-file', file);
    
        // AJAX request
        $.ajax({
            url: '/blog/create-blog/',
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },  // Include CSRF token in headers
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
    
                if (response.blog) {
                    let blog = response.blog;
    
                    // HTML structure for the new blog
                    let _html = `
                        <div class="card lg:mx-0 uk-animation-slide-bottom-small">
                            <!-- Post Header -->
                            <div class="flex justify-between items-center lg:p-4 p-2.5">
                                <div class="flex flex-1 items-center space-x-4">
                                    <a href="#">
                                        <img src="${blog.profile_image}" class="bg-gray-200 border border-white rounded-full w-10 h-10" />
                                    </a>
                                    <div class="flex-1 font-semibold capitalize">
                                        <a href="#" class="text-black dark:text-gray-100">${blog.user}</a>
                                        <div class="text-gray-700 flex items-center space-x-2">
                                            <span>${blog.date}</span>
                                            <ion-icon name="people"></ion-icon>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div uk-lightbox>
                                <div class="p-5 pt-0 border-b dark:border-gray-700 pb-3">${blog['blog-title']}</div>
                                <div class="grid grid-cols-2 gap-2 px-5">
                                    <a href="${blog['blog-file']}" class="col-span-2">
                                        <img src="${blog['blog-file']}" alt="" class="media rounded-md w-full lg:h-76 object-cover" />
                                    </a>
                                </div>
                            </div>
                            <div class="p-4 space-y-3">
                                <div class="flex space-x-4 lg:font-bold">
                                    <a class="flex items-center space-x-2 text-blue-500" style="cursor: pointer;">
                                        <div class="p-2 rounded-full lg:bg-gray-100 dark:bg-gray-600">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22">
                                                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                                            </svg>
                                        </div>
                                        <div>Like</div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
    
                    // Add new blog to the page
                    $(".blog-div").prepend(_html);
                    $("#blog-title").val('')
                    // Close the modal
                    $("#create-blog-modal").removeClass('uk-flex uk-open');

                }
            },
            error: function (error) {
                console.error('Error:', error);
                alert('An error occurred while creating the blog. Please try again.');
            }
        });
    });
    
    $(document).on('click', '#blog-like-btn', function(){
        let id = $(this).attr('data-blog-like-btn');
        console.log(id)

        $.ajax({
            url: "/blog/like-blog/",
            dataType:'json',
            data :{
                'id':id
            },
            success : function(response){
                if (response.data.bool === true){
                    console.log('Liked')
                    console.log(response.data.likes)
                    $("#blog-like-count"+id).text(response.data.likes)
                    $('.blog-like-btn'+id).addClass('text-blue-500')
                    $('.blog-like-btn'+id).removeClass('text-black')
                } else{
                    if(response.data.bool === false){
                        console.log('unliked');
                        console.log(response.data.likes)
                        $("#blog-like-count"+id).text(response.data.likes)
                        $('.blog-like-btn'+id).removeClass('text-blue-500')
                        $('.blog-like-btn'+id).addClass('text-black')
                        
                    }
                }
            }
        })
    });


    $(document).on('click', '#send-blog-comment', function(){
        console.log('Comment sent')
        let id = $(this).attr('data-send-blog-comment')
        let comment  = $('#blog-comment-input'+id).val()

        // console.log(id+ comment)

        $.ajax({
            url: '/blog/comment-blog/',
            method: 'GET',
            dataType: 'json',
            data: {
                'id': id,
                'comment': comment
            },
            success: function(response){
                console.log(response)
                let new_comment  = '<div class="flex">\
                                        <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                                            <img src="'+response.data.profile_image+'" alt="" class="absolute h-full rounded-full w-full" />\
                                        </div>\
                                        <div>\
                                            <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                                                <p class="leading-6">'+response.data.comment+'</p>\
                                                <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                                            </div>\
                                            <div class="text-xs flex items-center space-x-3 mt-2 ml-5">\
                                                <a id="like-blog-comment'+response.data.comment_id+'" data-like-blog-comment="'+response.data.comment_id+'" class="like-blog-comment text-gray-500" >\
                                                    <i id="like-comment-icon'+response.data.comment_id+'" class="fas fa-heart"></i>\
                                                </a> \
                                                <small>\
                                                    <span id="like-blog-comment-count'+response.data.comment_id+'">0</span>\
                                                </small>\
                                                <details >\
                                                    <summary>\
                                                    <div class="">Reply</div>\
                                                    </summary>\
                                                    <details-menu role="menu" class="origin-topf-right relative right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">\
                                                        <div class="pyf-1" role="none">\
                                                            <br>\
                                                        <div class="p-1 d-flex">\
                                                            \
                                                            <input type="text"  class="with-border blog-reply-input'+response.data.comment_id+'"  id="blog-reply-input'+response.data.comment_id+'">\
                                                            <button id="reply-blog-comment-btn" data-reply-blog-comment-btn="'+response.data.comment_id+'" type="submit" class="reply-blog-comment-btn block w-fulfl text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">\
                                                            <ion-icon name="send"></ion-icon>\
                                                        </button>\
                                                    </div>\
                                                    </div>\
                                                    </details-menu>\
                                                </details>\
                                                <span> '+response.data.date+' </span>\
                                            </div>\
                                            <div class="reply-div'+response.data.comment_id+'"></div>\
                                        </div>\
                                    </div>\
                                    '
                                    $("#blog-comment-div"+id).prepend(new_comment)
                                    $("#blog-comment-input"+id).val('')
                                    $("#blog-like-count"+id).text(response.data.comment_count)
                                    let remaining_comments = response.data.remaining_comments;
                                    let view_more_comment = $("#view-more-comments"+id)

                                    if (remaining_comments > 0){
                                        view_more_comment.html(
                                            `<a href="#" class="hover:text-blue-600 hover:underline">
                                                View ${remaining_comments} more Comment${remaining_comments > 1 ? 's' : ''}
                                            </a>
                                            `
                                        )
                                    }else{
                                        view_more_comment.html("<p class='text-blue-600'>No more comments </p>")
                                    }
            }
        })
    })

    $(document).on('click', '.like-blog-comment', function() {
        console.log('liked');
        let id = $(this).attr('data-like-blog-comment');
        console.log(id);
    
        $.ajax({
            url: '/blog/like-blog-comment/',
            dataType: 'json',
            data: {
                'id': id
            },
            success: function(response) {
                console.log(response);
                if (response.data.bool === true) {
                    $("#like-blog-comment-count" + id).text(response.data.likes);
                    $("#like-blog-comment" + id).css('color', 'red');
                } else {
                    $("#like-blog-comment-count" + id).text(response.data.likes);
                    $("#like-blog-comment" + id).css('color', 'gray');
                }
            }
        });
    });
    
    $(document).on('click', '#reply-blog-comment-btn', function(){
        console.log('replied')
        let id = $(this).attr('data-reply-blog-comment-btn')
        console.log(id)
        let reply = $('#blog-reply-input'+id).val()
        console.log(reply)

        $.ajax({
            url:'/blog/reply-blog-comment/',
            dataType:'json',
            data:{
                'id':id,
                'reply':reply
            },
            success : function(response){
                console.log(response)

                let new_reply = '<div class="flex mr-6" style="margin-right: 10px;">\
                                    <div class="w-5 h-5 rounded-full relative flex-shrink-0">\
                                        <img src="'+response.data.profile_image+'" style="width: 20px; height: 20px;" alt="" class="absolute h-full rounded-full w-full">\
                                    </div>\
                                    <div>\
                                        <div class="text-gray-700 py-1 px-1.5 rounded-md bg-gray-100 relative lg:ml-2.5 ml-1 lg:mr-6 dark:bg-gray-800 dark:text-gray-100">\
                                            <p class="leading-6 text-sm">'+response.data.reply+'</p>\
                                            <div class="absolute w-1.5 h-1.5 top-1.5 -left-0.5 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                                        </div>\
                                    </div>\
                                </div>\
                                '

                $(".reply-div"+id).prepend(new_reply)
                $(".blog-reply-input"+id).val('')
            }
        })
    })

    $(document).on('click', '#delete-blog-comment',function(){
        console.log('deleted')
        let id = $(this).attr('data-delete-blog-comment')
        console.log(id)

        $.ajax({
            url :'/blog/delete-blog-comment/',
            dataType:'json',
            data:{
                'id':id
            },
            success: function(response){
                console.log('comment deleted')
                $("#blog-comment-div"+id).addClass('d-none')
            }
        })
    })
})