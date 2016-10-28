import {Component} from '@angular/core';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <div id="head">
      <div id="nav">
        <searchbar></searchbar>
        <topnav></topnav>
      </div>
      <div class="col-xs-2" id="filter">
        <filters></filters>
      </div>
      <div class="col-xs-1"></div>
      <div id="body" class="col-xs-6">
        <router-outlet></router-outlet>
      </div>
      <div class="col-xs-3">
        <a routerLink="app/create-event" routerLinkActive="active" id="createicon" class="icon ion-plus-circled" title="Host a new event"></a>
      </div>
    </div>

    `,
    styleUrls: ['app/styles/master-styles.css'],
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent {
    private _open: boolean = false;

    private _toggleSidebar() {
        this._open = !this._open;
    }
}