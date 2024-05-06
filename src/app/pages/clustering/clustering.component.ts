import { Component } from '@angular/core';
import { Service } from '../../service.service';

@Component({
  selector: 'app-clustering',
  templateUrl: './clustering.component.html',
  styleUrls: ['./clustering.component.scss']
})
export class ClusteringComponent {
  destination: string = "";
  client: string = "";
  cluster: number | undefined;
  loading: boolean = false;

  constructor(private clusterService: Service) {}

  getCluster() {
    if (!this.destination || !this.client) {
      console.error("Destination and client are required.");
      return;
    }
    this.loading = true; // Set loading to true before making the request
    this.clusterService.getCluster(this.destination, this.client).subscribe(
      // (response: any) => {
      //   this.cluster = response.cluster;
      //   this.loading = false; // Set loading to false after receiving the response
      // },
      // (error: any) => {
      //   console.error("Error occurred while fetching cluster:", error);
      //   this.loading = false; // Ensure loading is set to false in case of an error
      // }
        {
          next: (data) => {
            this.cluster = data.cluster;
            // this.loading = false; // Set loading to false after receiving the response
          },
          error: (e) => {
            console.error("Error occurred while fetching cluster:", e);
            // this.loading = false; // Ensure loading is set to false in case of an error
          }
        }
    );
  }


}
