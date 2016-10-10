import { User }  from './user';


export class Event {
  id: number;
  title: string;
  host: User.name;
  date: string;
  maxGuests: number;
  locationName: string;
  locationAddress: string;
  tagName: string;
  description: string;
}
