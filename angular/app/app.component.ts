import {Component} from '@angular/core';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <a routerLink="/list-view" routerLinkActive="active">List View</a>
    <a routerLink="/create-event" routerLinkActive="active">Create Event</a>
    <a routerLink="/my-events" routerLinkActive="active">My Events</a>
    <router-outlet></router-outlet>
    <!--<list-view></list-view>-->
    `,
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent { }
