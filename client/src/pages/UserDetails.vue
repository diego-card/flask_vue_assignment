// src/views/UserPage.vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn
          text
          color="primary"
          @click="goBack"
          class="mb-4"
        >
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Users
        </v-btn>
      </v-col>
    </v-row>

    <v-card v-if="!loading">
      <v-card-title class="d-flex justify-space-between">
        <span class="text-h5">User Details: {{ user.username }}</span>
        <div>
          <v-btn
            color="primary"
            class="mr-2"
            @click="editUser"
          >
            <v-icon left>mdi-pencil</v-icon>
            Edit
          </v-btn>
          <v-btn
            color="error"
            @click="confirmDelete"
          >
            <v-icon left>mdi-delete</v-icon>
            Delete
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Username
              </v-list-item-title>
              <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Roles
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  v-for="role in user.roles"
                  :key="role"
                  color="primary"
                  small
                  class="mr-1"
                >
                  {{ role }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Timezone
              </v-list-item-title>
              <v-list-item-subtitle>{{ user.preferences?.timezone }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Status
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  :color="user.active ? 'success' : 'error'"
                  small
                >
                  {{ user.active ? 'Active' : 'Inactive' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Created At
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ formatDate(user.created_ts) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-bold">
                Last Updated
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ formatDate(user.updated_ts) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <v-skeleton-loader
      v-else
      type="card"
    ></v-skeleton-loader>

    <!-- Edit Dialog -->
    <v-dialog
      v-model="editDialog"
      max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">Edit User</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="editedItem.username"
              label="Username"
              :rules="[v => !!v || 'Username is required']"
              required
            ></v-text-field>

            <v-select
              v-model="editedItem.roles"
              :items="availableRoles"
              label="Roles"
              multiple
              chips
              :rules="[v => v.length > 0 || 'At least one role is required']"
            ></v-select>

            <v-text-field
              v-model="editedItem.preferences.timezone"
              label="Timezone"
              :rules="[v => !!v || 'Timezone is required']"
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
          <v-btn
            color="grey darken-1"
            text
            @click="closeEdit"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="saveEdit"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog
      v-model="deleteDialog"
      max-width="400px"
    >
      <v-card>
        <v-card-title class="text-h5">
          Delete User
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete this user? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey darken-1"
            text
            @click="closeDelete"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            text
            @click="deleteUser"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserPage',

  data: () => ({
    loading: true,
    user: {},
    editDialog: false,
    deleteDialog: false,
    valid: true,
    editedItem: {
      username: '',
      roles: [],
      preferences: {
        timezone: ''
      },
      active: true
    },
    availableRoles: ['admin', 'manager', 'tester']
  }),

  created() {
    this.fetchUser()
  },

  methods: {
    async fetchUser() {
      this.loading = true
      try {
        const response = await axios.get(`/users/${this.$route.params.id}`)
        this.user = response.data
      } catch (error) {
        console.error('Error fetching user:', error)
      } finally {
        this.loading = false
      }
    },

    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      return new Date(timestamp).toLocaleString()
    },

    goBack() {
      this.$router.push({ name: 'Users' })
    },

    editUser() {
      this.editedItem = JSON.parse(JSON.stringify(this.user))
      this.editDialog = true
    },

    async saveEdit() {
      if (!this.$refs.form.validate()) return

      if (!confirm('Are you sure you want to save these changes?')) {
        return
      }

      try {
        const { _id, ...userData } = this.editedItem;  // Destructure to exclude _id and avoid error
        const response = await axios.put(`/users/${_id.$oid}`, userData);
        this.user = response.data
        this.editDialog = false

        this.$router.go(0);
      } catch (error) {
        console.error('Error updating user:', error)
      }
    },

    closeEdit() {
      this.editDialog = false
      this.$refs.form.reset()
    },

    confirmDelete() {
      this.deleteDialog = true
    },

    closeDelete() {
      this.deleteDialog = false
    },

    async deleteUser() {
      try {
        await axios.delete(`/users/${this.user._id.$oid}`)
        this.deleteDialog = false
        this.$router.push({ name: 'Users' })
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    }
  }
}
</script>