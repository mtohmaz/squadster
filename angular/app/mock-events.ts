import { Event } from './event';

export const EVENTS: Event[] = [
  { id:1, title: 'Bowling', location: 'AMC', startDate: '09/25/2016', startTime: '9:00pm', currentAttendees: 3, maxAttendees: 10, description: 'Meeting new people at bowling.'},
  { id:2, title: 'Dinner', location: 'El Toro', startDate: '09/30/2016', startTime: '9:00pm', currentAttendees: 9, maxAttendees: 10, description: 'Meeting new people for dinner.'},
  { id:3, title: 'Movie', location: 'My apartment', startDate: '10/25/2016', startTime: '9:00pm', currentAttendees: 0, maxAttendees: 2, description: 'Netflix and chill.'}
];
