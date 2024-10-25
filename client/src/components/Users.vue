// UsersPage.vue
<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="openCreateDialog">
          Add New User
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="users"    
      :loading="loading"
      class="elevation-1"
    >
      <template v-slot:item.username="{ item }">
        <v-btn
          text
          color="primary"
          @click="goToUserDetails(item._id.$oid)"
        >
          {{ item.username }}
        </v-btn>
      </template>

      <template v-slot:item.roles="{ item }">
        <v-chip
          v-for="role in item.roles"
          :key="role"
          class="mr-1"
          small
        >
          {{ role }}
        </v-chip>
      </template>

      <template v-slot:item.active="{ item }">
        <v-chip :color="item.active ? 'green' : 'red'" small>
          {{ item.active ? 'Active' : 'Inactive' }}
        </v-chip>
      </template>

      <template v-slot:item.updated_ts="{ item }">
          {{ formatDate(item.updated_ts) }}
      </template>

      <template v-slot:item.created_ts="{ item }">
          {{ formatDate(item.created_ts) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editUser(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="confirmDelete(item)">
          mdi-delete
        </v-icon>
      </template>      
    </v-data-table>

    <!-- User Form Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span>{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.username"
              label="Username"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.password"
              label="Password"
              type="password"
              required
            ></v-text-field>
            <v-select
              v-model="editedItem.roles"
              :items="availableRoles"
              label="Roles"
              multiple
              chips
            ></v-select>
            <v-text-field
              v-model="editedItem.preferences.timezone"
              label="Timezone"
              required
            ></v-text-field>
            <v-switch
              v-model="editedItem.active"
              label="Active"
            ></v-switch>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Delete User</v-card-title>
        <v-card-text>
          Are you sure you want to delete this user?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deleteItemConfirm">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UsersPage',
  data: () => ({
    loading: false,
    dialog: false,
    deleteDialog: false,
    saveDialog: false,
    valid: true,
    headers: [
      { title: 'Username', value: 'username' },
      { title: 'Roles', value: 'roles' },
      { title: 'Timezone', value: 'preferences.timezone' },
      { title: 'Is Active?', value: 'active' },
      { title: 'Last Updated At', value: 'updated_ts' },
      { title: 'Created At', value: 'created_ts' },
      { title: 'Actions', value: 'actions', sortable: false }
    ],
    users: [],
    editedIndex: -1,
    editedItem: {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: ''
      },
      active: true
    },
    defaultItem: {
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: ''
      },
      active: true
    },
    availableRoles: ['admin', 'manager', 'tester']    
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New User' : 'Edit User'
    },
  },

  mounted() {
    this.fetchUsers()
  },

  methods: {
    // 
    goToUserDetails(userId) {
      this.$router.push({
        name: 'UserDetails',
        params: { id: userId }
      })
    },
    //
    async fetchUsers() {
      this.loading = true
      try {
        const response = await axios.get('/users')
        this.users = response.data
        
      } catch (error) {
        console.error('Error fetching users:', error)
      } finally {
        this.loading = false
      }
    },

    openCreateDialog() {
      this.editedIndex = -1
      this.editedItem = Object.assign({}, this.defaultItem)
      this.dialog = true
    },
    editUser(item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    confirmDelete(item) {
      this.editedItem = Object.assign({}, item)
      this.deleteDialog = true
    },
    confirmSave() {
      if (!this.$refs.form.validate()) return
      this.saveDialog = true
    },

    async deleteItemConfirm() {
      try {
        await axios.delete(`/users/${this.editedItem._id.$oid}`)
        this.users.splice(this.users.indexOf(this.editedItem), 1)
      } catch (error) {
        console.error('Error deleting user:', error)
      }
      this.deleteDialog = false
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    async save() {
      if (!this.$refs.form.validate()) return

      if (!confirm('Are you sure you want to save these changes?')) {
        return
      }

      try {
        if (this.editedIndex > -1) {
          // Update
          const { _id, ...userData } = this.editedItem;  // Destructure to exclude _id and avoid error
          const response = await axios.put(`/users/${_id.$oid}`, userData);    
          Object.assign(this.users[this.editedIndex], response.data)
        } else {
          // Create
          const response = await axios.post('/users', this.editedItem)
          this.users.push(response.data)      
          await this.fetchUsers()
        }
        this.saveDialog = false
        this.close()
      } catch (error) {
        console.error('Error saving user:', error)
      }
    },

    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      return new Date(timestamp).toLocaleString()
    },
  }
}
</script>
