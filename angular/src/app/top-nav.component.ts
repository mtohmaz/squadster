import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
    selector: "topnav",
    templateUrl: 'html/top-nav.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['styles/top-nav.component.css', 'styles/mapswitch.css'],
})

export class TopNavComponent implements OnInit{
    private _open: boolean = false;
    isChecked = false;

    constructor(
        private router: Router,
        private route: ActivatedRoute
    ) { }

    ngOnInit() {
        this.check();
    }

    isEdited() {
        if (this.router.url.search("/app/list-view") == 0 || this.router.url.search("/app/map-view") == 0)
            return true;
        return false;
    }

    check() {
        if (this.router.url.search("/app/list-view") == 0) {
            this.isChecked = false;
        }
        else if (this.router.url.search("app/map-view") == 0) {
            this.isChecked = true;
        }
        return this.isChecked;
    }

    toggle() {
        this.route.queryParams.forEach((params: Params) => {
            if (this.router.url.search("/app/list-view") == 0) {
                this.router.navigate(["app/map-view"], {queryParams: params});
            }
            else {
                this.router.navigate(["app/list-view"], {queryParams: params});
            }
        });
    }
}
