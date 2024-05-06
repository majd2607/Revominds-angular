import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClusteringComponent } from './clustering.component';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    ClusteringComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild([
      {
        path: '',
        component: ClusteringComponent,
      },
    ]),
  ]
})
export class ClusteringModule { }
