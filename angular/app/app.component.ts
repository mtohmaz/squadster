import {Component} from '@angular/core';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <div id="head">

      <div id="nav">
        <topnav></topnav>
      </div>
      <div id="body">
        <router-outlet></router-outlet>
      </div>
    </div>

    <ng2-sidebar class="sidebar"
        [(open)]="_open" 
        [closeOnClickOutside]="true"
        [showOverlay]="true">
      <sidenav></sidenav>
    </ng2-sidebar>

    <a (click)="_toggleSidebar()" class="menu icon ion-navicon-round">Menu</a>
    <a routerLink="app/create-event" routerLinkActive="active" class="create icon ion-plus-circled" title="Create a new event"></a>
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
