import {Component, ViewEncapsulation, OnInit} from "@angular/core";

@Component({
    selector: "searchbar",
    template: `
    <div class="row" id="searchbar">
        <div class="col-xs-3">
            <div id="logo">
                  <img src="../images/SquadsterLogo.png" />
            </div>
        </div>
        <div class="col-xs-6">
            <input type="text" class="searchbox" placeholder="Search for events...">
            <i class="icon ion-search"></i>
        </div>
        <div class="col-xs-3"></div>
    </div>
    `,
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/search-bar.component.css'],
})

export class SearchBarComponent { }
