import {Component, ViewEncapsulation, OnInit} from "@angular/core";

@Component({
    selector: "searchbar",
    template: `
    <div class="row" id="searchbar">
        <div class="col-xs-2">
            <div id="logo">
                  <img src="../images/SquadsterLogo.png" />
            </div>
        </div>
        <div class="col-xs-6">
            <input type="text" class="searchbox" placeholder=" Find an event nearby...">
        </div>
        <div class="col-xs-2">
            <button type="button" class="btn btn-warning btn-lg" routerLink="app/create-event" routerLinkActive="active">Host a New Event</button>
        </div>
        <div class="col-xs-2">
            <button type="button" class="btn btn-success icon ion-person" routerLink="app/login" routerLinkActive="active"> My Account</button>
        </div>
    </div>
    `,
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/search-bar.component.css'],
})

export class SearchBarComponent { }
