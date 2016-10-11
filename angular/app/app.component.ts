import {Component} from '@angular/core';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <!--<a routerLink="/list-view" routerLinkActive="active">List View</a>
    <a routerLink="/create-event" routerLinkActive="active">Create Event</a>
    <a routerLink="/my-events" routerLinkActive="active">My Events</a>-->
    <div id="head">

      <div id="nav">
        <topnav></topnav>
        <sidenav></sidenav>
      </div>
      <div id="body">
        <router-outlet></router-outlet>
      </div>
    </div>
    <!--<list-view></list-view>-->
    `,
    styleUrls: ['app/styles/master-styles.css'],
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent { }
