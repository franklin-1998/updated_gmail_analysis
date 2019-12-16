import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from "@angular/common/http";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCardModule, MatIconModule, MatToolbarModule, MatButtonModule, MatFormFieldModule, MatInputModule } from '@angular/material';
import { AppRoutingModule} from './app-routing.module';
import { AppComponent } from './app.component';
import { FusionChartsModule } from 'angular-fusioncharts';

import * as FusionCharts from 'fusioncharts';
// Load Charts module
import * as Charts from 'fusioncharts/fusioncharts.charts';
// Load fusion theme
import { RouterModule } from '@angular/router';
import * as FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';

import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { AllComponent } from './all/all.component';
import { SelectedComponent } from './selected/selected.component';


// Add dependencies to FusionChartsModule
FusionChartsModule.fcRoot(FusionCharts, Charts, FusionTheme);

@NgModule({
  declarations: [
    AppComponent,
    AllComponent,
    SelectedComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatInputModule,
    FusionChartsModule,  
    RouterModule.forRoot([  
      { path: 'all', component: AllComponent },
      { path: 'selected', component: SelectedComponent },
     ])
  
    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
