// import { Calendar } from '@fullcalendar/core';
// import dayGridPlugin from '@fullcalendar/daygrid';
// import timeGridPlugin from '@fullcalendar/timegrid';
// import interactionPlugin from '@fullcalendar/interaction';

// document.addEventListener('DOMContentLoaded', function () {
//     const calendarEl = document.getElementById('calendar');

//     const calendar = new Calendar(calendarEl, {
//         plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
//         initialView: 'dayGridMonth',
//         headerToolbar: {
//             left: 'prev,next today',
//             center: 'title',
//             right: 'dayGridMonth,timeGridWeek,timeGridDay',
//         },
//         eventClick: function (info) {
//             // Handle event click
//         },
//         events: function (fetchInfo, successCallback, failureCallback) {
//             fetch('/get_client_appointments/', {
//                 method: 'GET',
//                 credentials: 'same-origin',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-Requested-With': 'XMLHttpRequest',
//                 },
//             })
//                 .then(function (response) {
//                     return response.json();
//                 })
//                 .then(function (events) {
//                     console.log('Events fetched:', events);
//                     successCallback(events);
//                 })
//                 .catch(function (error) {
//                     console.error('Error fetching events:', error);
//                     failureCallback(error);
//                 });
//         },
        
//     });

//     calendar.render();
// });
