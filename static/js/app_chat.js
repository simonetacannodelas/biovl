(function() {
    'use strict';
    // ----------------------------------------------------
    // Targeted Elements
    // ----------------------------------------------------

    const chatPage   = $(document)
    const chatWindow = $('.chatbubble')
    const chatHeader = chatWindow.find('.unexpanded')
    const chatBody   = chatWindow.find('.chat-window')


    // ----------------------------------------------------
    // Register helpers
    // ----------------------------------------------------

    let helpers = {
        getBotResponse: function() {
          var rawText = $("#textInput").val();
          var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
          $("#textInput").val("");
          $("#chatbox").append(userHtml);
          document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
          $.get("/frosty_answer", { msg: rawText }).done(function(data) {
            var botHtml = '<p class="botText"><span>' + data + '</span></p>';
            $("#chatbox").append(botHtml);
            document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
          });
        }
        $("#textInput").keypress(function(e) {
            if(e.which == 13) {
                getBotResponse();
            }
        });
        $("#buttonInput").click(function() {
          getBotResponse();
        }

    // ----------------------------------------------------
    // Toggles the display of the chat window.
    // ----------------------------------------------------
        ToggleChatWindow: function () {
            chatWindow.toggleClass('opened')
            chatHeader.find('.title').text(
                chatWindow.hasClass('opened') ? 'Minimize Chat Window' : 'Chat with Support'
            )
        },
    // --------------------------------------------------------------------
    // Show the appropriate display screen. Login screen or Chat screen.
    // --------------------------------------------------------------------

        ShowAppropriateChatDisplay: function () {
            (chat.name) ? helpers.ShowChatRoomDisplay() : helpers.ShowChatInitiationDisplay()
        },

    // ----------------------------------------------------
    // Show the enter details form.
    // ----------------------------------------------------

        ShowChatInitiationDisplay: function () {
            chatBody.find('.chats').removeClass('active')
            chatBody.find('.login-screen').addClass('active')
        },

    // ----------------------------------------------------
    // Show the chat room messages display.
    // ----------------------------------------------------

        ShowChatRoomDisplay: function () {
            chatBody.find('.chats').addClass('active')
            chatBody.find('.login-screen').removeClass('active')

            setTimeout(function(){
                chatBody.find('.loader-wrapper').hide()
                chatBody.find('.input, .messages').show()
            }, 2000)
        },

    // ----------------------------------------------------
    // Append a message to the chat messages UI.
    // ----------------------------------------------------

        NewChatMessage: function (message) {
            if (message !== undefined) {
                const messageClass = message.sender !== chat.email ? 'support' : 'user'

                chatBody.find('ul.messages').append(
                    `<li class="clearfix message ${messageClass}">
                        <div class="sender">${message.name}</div>
                        <div class="message">${message.text}</div>
                    </li>`
                )


                chatBody.scrollTop(chatBody[0].scrollHeight)
            }
        },

    // ----------------------------------------------------
    // Send a message to the chat channel.
    // ----------------------------------------------------

        SendMessageToSupport: function (evt) {

            evt.preventDefault()

            let createdAt = new Date()
            createdAt = createdAt.toLocaleString()

            const message = $('#newMessage').val().trim()

            chat.myChannel.trigger('client-guest-new-message', {
                'sender': chat.name,
                'email': chat.email,
                'text': message,
                'createdAt': createdAt
            });

            helpers.NewChatMessage({
                'text': message,
                'name': chat.name,
                'sender': chat.email
            })

            console.log("Message added!")

            $('#newMessage').val('')
        },

    // ----------------------------------------------------
    // Logs user into a chat session.
    // ----------------------------------------------------

        LogIntoChatSession: function (evt) {
            const name  = $('#fullname').val().trim()
            const email = $('#email').val().trim().toLowerCase()

            // Disable the form
            chatBody.find('#loginScreenForm input, #loginScreenForm button').attr('disabled', true)

            if ((name !== '' && name.length >= 3) && (email !== '' && email.length >= 5)) {
                axios.post('/new/guest', {name, email}).then(response => {
                    chat.name = name
                    chat.email = email
                    chat.myChannel = pusher.subscribe('private-' + response.data.email);
                    helpers.ShowAppropriateChatDisplay()
                })
            } else {
                alert('Enter a valid name and email.')
            }

            evt.preventDefault()
        }
    }

    // ------------------------------------------------------------------
    // Listen for a new message event from the admin
    // ------------------------------------------------------------------

    // ----------------------------------------------------
    // Register page event listeners
    // ----------------------------------------------------

    chatPage.ready(helpers.getBotResponse)
    chatHeader.on('click', helpers.ToggleChatWindow)
    chatBody.find('#messageSupport').on('submit', helpers.SendMessageToSupport)
}())

// (function getBotResponse() {
//           var rawText = $("#textInput").val();
//           var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
//           $("#textInput").val("");
//           $("#chatbox").append(userHtml);
//           document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
//           $.get("/frosty_answer", { msg: rawText }).done(function(data) {
//             var botHtml = '<p class="botText"><span>' + data + '</span></p>';
//             $("#chatbox").append(botHtml);
//             document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
//           });
//         }
//         $("#textInput").keypress(function(e) {
//             if(e.which == 13) {
//                 getBotResponse();
//             }
//         });
//         $("#buttonInput").click(function() {
//           getBotResponse();
//         })
// )