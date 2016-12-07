export class Event {
  event_id: number;
  host_id: number;
  title: string;
  //hostName: string;
  location: string;
  lat: number;
  lon: number;
  date: Date;
  comments: string;
  coordinates: string;
  //startTime: string;
  //currentAttendees: number;
  max_attendees: number;
  description: string;
  summary_fields: {
    host_email: string;
    number_of_attendees: number;
  }
}
