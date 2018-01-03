// app.js
// if useMessenger is false, the plugin will not make graphAPI calls to facebook
// if useLocalChat is true, the plugin will initialize the local chat view.
Bot.init(
    config.FBChatToken || '',
    'SETUP_PLAY_GO_THIS_IS_RIGHT',
    false, // useMessenger
    config.useFBChatLocalTest || false);

// Bot.on('text', async(event: object) => {
//     // do something
// });

// Bot.on('attachments', async(event: object) => {
//     // do something
// });

// Bot.on('postback', async(event: object) => {
//     // do something
// });

app.use('/webhook', Bot.router());
// go to http://localhost:5000/webhook/localChat/ for local chat debugging