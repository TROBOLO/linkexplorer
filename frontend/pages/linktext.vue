<template>
  <div class="text-center">
    <div class="row">
    <div class="col-md-4">
      <input
        class="searchField"
        type="text"
        v-model="input"
        placeholder="Enter your linktext..."
      />
    </div>
    <div class="col-md-4">
      <input
        class="searchField"
        type="text"
        v-model="exclude"
        placeholder="Exclude linktext..."
      />
      
    </div>
    </div>

    <table
      class="table-responsive table table-striped"
      v-if="input.length >= 3"
    >
      <thead>
        <tr>
          <th>Linktext</th>
          <th>Link Source</th>
          <th>Link Target</th>
        </tr>
      </thead>
      <tbody>
        <tr
          class="text-left"
          v-for="(link, index) in filteredLinks"
          :key="index"
        >
          <td>{{ link.link_text }}</td>
          <td style="padding-left: 10"><a target="_blank" :href="link.link_source">{{ link.link_source }}</a></td>
          <td><a target="_blank" :href="link.link_target">{{ link.link_target }}</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import data from "~/assets/data/links.json";
var links = data.links.filter((link) => link.link_target !== null);

export default {
  data() {
    return {
      input: "",
      exclude: "",
      links,
    };
  },
  computed: {
    filteredLinks() {
      const input = this.input.toLowerCase();
      const exclude = this.exclude.toLowerCase();

      if (this.input.length >= 3) {
        return this.links.filter((link) => {

          if (exclude.length >= 3) {
            return (
              link.link_text.toLowerCase().includes(input) &&
              !link.link_text.toLowerCase().includes(exclude)
            );
          } else {
            return link.link_text.toLowerCase().includes(input);
          }

          // return link.link_text
          //   .toLowerCase()
          //   .includes(this.input.toLowerCase());
        });
      }
    },
  },
};
</script>

<style scoped>
.searchField {
  margin-top: 10px;
  width: 100%;
  height: 50px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  font-size: 20px;
  margin-bottom: 20px;
}

/* remove all a href link styles in the table */
table a {
  color: inherit;
  text-decoration: none;
}

</style>
