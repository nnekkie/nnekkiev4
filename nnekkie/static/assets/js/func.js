console.log("Collecting snaps data");

$(document).ready(function(){
    $("#snaps-form").submit(function(e){
        e.preventDefault();
        console.log("Processing Snaps");

        // Collect form data
        let snaps_visibility = $("#visibility").val();
        let fileInput = $("#snaps-video")[0];
        let file = fileInput.files[0];
        let fileName = file ? file.name : '';

        console.log(snaps_visibility);
        console.log(fileName);

        let formData = new FormData();
        formData.append("snaps-video", file, fileName);
        formData.append("visibility", snaps_visibility);
        
        $.ajax({
            url: "/create-snaps/",
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log("Snap uploaded successfully!", data);
                if (data.snaps) {
                    addNewSnap(data.snaps); // Call the function to add the snap
                    closeSnap(); // Close the snap UI after success
                } else {
                    alert('Error: ' + data.error);
                }
            },
            error: function(xhr, status, error) {
                console.error("Upload failed:", error);
                alert("Failed to upload snap. Please try again.");
            }
        });
        
        // Function to dynamically add a new snap to the DOM
        function addNewSnap(snap) {
            // Create the story HTML
            let storyHTML = `
                <a href="#create-post" uk-toggle="target: body ; cls: story-active">
                    <div class="single_story">
                        ${snap.video ? `<video controls><source src="${snap.video}" type="video/mp4"></video>` : ''}
                        <div class="story-avatar">
                            <img src="${snap.profile_image}" alt="">
                        </div>
                        <div class="story-content">
                            <h4>${snap.full_name}</h4>
                            <p>${snap.date} ago</p>
                        </div>
                    </div>
                </a>
            `;
            $(".user_story").prepend(storyHTML);
        
            // Create the story list HTML (for time display)
            let storyListHTML = `
                <a href="#">
                    <div class="story-media">
                        <img src="${snap.profile_image}" alt="">
                    </div>
                    <div class="story-text">
                        <div class="story-username">${snap.full_name}</div>
                        <p>
                            <span class="story-count">1 new</span>
                            <span class="story-time">just now</span>
                        </p>
                    </div>
                </a>
            `;
            $(".story-users-list").prepend(storyListHTML);
        
            // Slider HTML (for lightbox)
            let sliderHTML = `
                <li class="relative">
                    <span uk-switcher-item="previous" class="slider-icon is-left"></span>
                    <span uk-switcher-item="next" class="slider-icon is-right"></span>
                    <div uk-lightbox>
                        ${snap.video ? `<a href="${snap.video}" data-alt="Video">
                            <video class="story-slider-image" controls>
                                <source src="${snap.video}" type="video/mp4">
                            </video>
                        </a>` : ''}
                        <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">
                            <input placeholder="Add your Comment..." class="bg-transparent max-h-10 shadow-none px-5">
                            <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">
                                <a style="cursor: pointer;">
                                    <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>
                                </a>
                            </div>
                        </div>
                    </div>
                </li>
            `;
            $("#story_slider").prepend(sliderHTML);
        
            // Re-initialize UIkit components (critical for dynamic content)
            UIkit.switcher($("#story_slider")); // Re-init switcher for slider
            UIkit.lightbox($("#story_slider")); // Re-init lightbox for videos
        }
        
        // Function to close the snap UI
        function closeSnap() {
            console.log("Closing the snap form..."); // Debug log
            $("#create-snaps-modal").removeClass("uk-flex uk-open")// Remove UIkit classes and hide the form
        }
    });

    // Function to dynamically add new snap to the DOM
    function addNewSnap(snap) {
        let storyHTML = `
            <a href="#create-post" uk-toggle="target: body ; cls: story-active">
                <div class="single_story">
                    ${snap.video ? `<video controls><source src="${snap.video}" type="video/mp4"></video>` : ''}
                    <div class="story-avatar">
                        <img src="{% if request.user.profile.image %}{{ request.user.profile.image.url }}{% endif %}" alt="">
                    </div>
                    <div class="story-content">
                        <h4>${snap.full_name}</h4>
                        <p>${snap.date} ago</p>
                    </div>
                </div>
            </a>
        `;

        $(".user_story").prepend(storyHTML);

        // Story List (for time display)
        let storyListHTML = `
            <a href="#">
                <div class="story-media">
                    <img src="{% if request.user.profile.image %}{{ request.user.profile.image.url }}{% endif %}" alt="">
                </div>
                <div class="story-text">
                    <div class="story-username">${snap.full_name}</div>
                    <p>
                        <span class="story-count"> 1 new </span>
                        <span class="story-time"> just now</span>
                    </p>
                </div>
            </a>
        `;
        $(".story-users-list").prepend(storyListHTML);

        // Slider (for lightbox)
        let sliderHTML = `
            <li class="relative">
                <span uk-switcher-item="previous" class="slider-icon is-left"></span>
                <span uk-switcher-item="next" class="slider-icon is-right"></span>
                <div uk-lightbox>
                    ${snap.video ? `<a href="${snap.video}" data-alt="Video">
                        <video class="story-slider-image" controls>
                            <source src="${snap.video}" type="video/mp4">
                        </video>
                    </a>` : ''}
                    <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">
                        <input placeholder="Add your Comment..." class="bg-transparent max-h-10 shadow-none px-5">
                        <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">
                            <a style="cursor: pointer;">
                                <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>
                            </a>
                        </div>
                    </div>
                </div>
            </li>
        `;
        $("#create-snaps-form").removeClass("uk-flex uk-open")
        $("#story_slider").prepend(sliderHTML);

        // Re-initialize UIkit components (critical)
        UIkit.switcher($("#story_slider"));  // Re-init switcher for slider
        UIkit.lightbox($("#story_slider"));  // Re-init lightbox for videos
    }
});
//group-realted oject
$(document).ready(function(){
    $(document).on("click","#group-like-btn", function(){
        console.log("liked")
        var btn_val  = $(this).attr("data-group-like-btn")
        console.log(btn_val)

        $.ajax({
            url : '/like-group-post/',
            dataType : 'json',
            data : {
                "id":btn_val
            },
            success : function(response){
                if (response.data.bool === true){
                    console.log('likes : ',response.data.likes);
                    $("#group-like-count"+ btn_val).text(response.data.likes)
                    $(".group-like-btn"+ btn_val).addClass("text-blue-500")
                    $(".group-like-btn"+ btn_val).removeClass("text-black")
                }else {
                    console.log('likes : ',response.data.likes);
                    $("#group-like-count"+ btn_val).text(response.data.likes)
                    $(".group-like-btn"+ btn_val).addClass("text-black")
                    $(".group-like-btn"+ btn_val).removeClass("text-blue-500")
                }
                
            }
        })
    });

    //comment on post

    $(document).on("click", "#group-comment-btn",function(){
        console.log('comment sent')
        let id = $(this).attr("data-group-comment-btn")
        let comment = $("#group-comment-input" + id).val()
        console.log(id)
        console.log(comment)

        $.ajax({
            url:'/comment-group-post/',
            dataType: 'json',
            data : {
                'id':id,
                'group-comment':comment
            },
            success:function(res){
                console.log(res)
                let _new_comment = '<div class="border-t py-4 space-y-4 dark:border-gray-600">\
                    <div class="flex card shadow p-0.5">\
                        <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                            <img src="'+res.data.profile_image+'" alt="" class="absolute h-full rounded-full w-full" />\
                        </div>\
                        <div>\
                            <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                                <p class="leading-6">'+res.data.comment+' <urna class="i uil-heart"></urna> <i class="uil-grin-tongue-wink"> </i></p>\
                                <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                            </div>\
                            <div class="text-sm flex items-center space-x-3 mt-2 ml-5">\
                                <small><span id="comment-like-count'+res.data.comment_id+'"> 0</span></small>\
                                <a id="like-group-comment-btn" data-like-group-comment="'+res.data.comment_id+'" class="like-group-comment'+res.data.comment_id+'   text-gray-500 " style="cursor: pointer;">\
                                    <i class="uil-heart like-group-comment{{c.id}}"></i> Love\
                                </a>\
                                <details>\
                                    <summary><div class="">Reply</div></summary>\
                                                        \
                                    <details-menu role="menu" class="origin-topf-right relative right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">\
                                        <div class="pyf-1" role="none">\
                                            <div method="POST" class="p-1 d-flex" action="#" role="none">\
                                                <input type="text" class="with-border" name="" id="group-reply-input'+res.data.comment_id+'" />\
                                                <button id="group-reply-comment-btn" data-group-reply-comment-btn="'+res.data.comment_id+'" class="block w-fulfl text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 group-reply-comment-btn'+res.data.comment_id+'" role="menuitem">\
                                                    <ion-icon name="send"></ion-icon>\
                                                </button>\
                                            </div>\
                                        </div>\
                                    </details-menu>\
                                </details>\
                                <span> <small>'+res.data.date+'</small> </span>\
                            </div>\
                        </div>\
                        <div class="reply-div'+res.data.comment_id +'">\
                    </div>\
                </div>\
                '

                $("#comment-div"+id).prepend(_new_comment)
                $("#comment-input"+id).val("")
                $("#comment-count"+id).text(res.data.comment_count)
            }
        })
    });
    // like grouppos comment feature

    $(document).on('click', "#like-group-comment-btn", function(){
        console.log("comment liked")
        let id = $(this).attr("data-like-group-comment")
        console.log('comment id', id)

        $.ajax({
            url :'/like-comment-group-post/',
            dataType:'json',
            data :{
                'id':id
            },
            success:function(res){
                console.log(res)
                if(res.data.bool === true){
                    $("#comment-like-count"+id).text(res.data.likes)
                    $(".like-group-comment" + id).addClass("text-blue-500")
                    $(".like-group-comment" + id).removeClass("text-gray-500")
                }else{
                    $("#comment-like-count"+id).text(res.data.likes)
                    $(".like-group-comment" + id).addClass("text-gray-500")
                    $(".like-group-comment" + id).removeClass("text-blue-500")
                }
            }
        });
    });

    $(document).on("click", "#group-reply-comment-btn", function(){
        console.log("reply sent")
        let id = $(this).attr("data-group-reply-comment-btn")
        let reply = $("#group-reply-input"+id).val()
        console.log(id)
        console.log(reply)

        $.ajax({
            url :'/reply-comment-group-post/',
            dataType:'json',
            data:{
                'id':id,
                'reply': reply
            },
            success: function(response){
                let new_reply = '<div class="flex mr-12 mb-2 mt-2 " style="margin-right: 20px;">\
                        <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                            <img src="'+response.data.profile_image+'" style="width: 40px; height: 40px;" alt="" class="absolute h-full rounded-full w-full" />\
                        </div>\
                        <div>\
                            <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                                <p class="leading-6">'+response.data.reply+'</p>\
                                <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                            </div>\
                        </div>\
                    </div>\
                '
                
                $(".reply-div"+id).prepend(new_reply)
                $("#group-reply-input"+id).val("")
            }
        })
    })

    //group post delete feature

    $(document).on("click", "#delete-group-comment", function(){
        console.log('comment deleted')

        let id = $(this).attr("data-delete-group-comment")
        console.log(id)

        $.ajax({
            url:'/delete-group-post-comment/',
            dataType:'json',
            data : {
                'id':id
            },
            success : function(response){
                console.log('comment ', id, ' deleted')
                $("#group-comment-div"+id).addClass("d-none")
            }
        })
    })
   
   
})


