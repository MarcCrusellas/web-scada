const socket = new WebSocket('ws://localhost:8080');

socket.onopen = () => {
    console.log('WebSocket connection established');
};

const sendHelloButton = document.getElementById('sendHello');
const requestNotificationButton = document.getElementById('requestNotification');

sendHelloButton.addEventListener('click', () => {
    socket.send('hello');
});

requestNotificationButton.addEventListener('click', () => {
    socket.send('notify');
});

socket.onmessage = (event) => {
    if (event.data.startsWith('notification:')) {
        const message = event.data.replace('notification:', '');
        const notificationDiv = document.createElement('div');
        notificationDiv.textContent = message;
        document.body.appendChild(notificationDiv);
    } else {
        console.log('Message from server:', event.data);
    }
};
