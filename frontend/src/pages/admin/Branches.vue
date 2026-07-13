<template>
    <DashboardLayout>
        <PageTitle title="Branch Management" />

        <form class="row g-2 mb-4" @submit.prevent="saveBranch">
            <div class="col-md-8">
                <input v-model="name" class="form-control" placeholder="Branch name" required>
            </div>
            <div class="col-md-4 d-flex gap-2">
                <button class="btn btn-primary" :disabled="saving">
                    {{ saving ? "Saving..." : editing ? "Update Branch" : "Add Branch" }}
                </button>
                <button v-if="editing" type="button" class="btn btn-outline-secondary" @click="cancelEdit">
                    Cancel
                </button>
            </div>
        </form>

        <Loader v-if="loading" />
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <EmptyState v-else-if="branches.length === 0" message="No branches found." />

        <DashboardTable v-else title="Branches">
            <template #head>
                <th>ID</th>
                <th>Name</th>
                <th>Actions</th>
            </template>
            <template #body>
                <tr v-for="branch in branches" :key="branch.id">
                    <td>{{ branch.id }}</td>
                    <td>{{ branch.name }}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-2" @click="editBranch(branch)">Edit</button>
                        <button class="btn btn-sm btn-outline-danger" @click="deleteBranch(branch.id)">Delete</button>
                    </td>
                </tr>
            </template>
        </DashboardTable>
    </DashboardLayout>
</template>

<script>
import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"
import { showToast } from "@/utils/toast"

export default {
    components: { DashboardLayout, DashboardTable, PageTitle, Loader, EmptyState },

    data() {
        return {
            branches: [],
            loading: true,
            saving: false,
            editing: null,
            name: "",
            error: ""
        }
    },

    async mounted() {
        await this.fetchBranches()
    },

    methods: {
        async fetchBranches() {
        this.loading = true
        this.error = ""

        try {
            const response = await api.get("/branches")
            this.branches = response.data
        } catch (error) {
            this.error = error.response?.data?.message || "Failed to load branches"
        } finally {
            this.loading = false
        }
        },

        editBranch(branch) {
            this.editing = branch
            this.name = branch.name
        },

        cancelEdit() {
            this.editing = null
            this.name = ""
        },

        async saveBranch() {
            this.saving = true

            try {
                if(this.editing){
                    await api.put("/branches/"+this.editing.id,{name:this.name})
                    showToast("Branch updated successfully","success")
                }else{
                    await api.post("/branches",{name:this.name})
                    showToast("Branch created successfully","success")
                }

                this.cancelEdit()
                await this.fetchBranches()
            } catch (error) {
                showToast(error.response?.data?.message || "Failed to save branch","danger")
            } finally {
                this.saving = false
            }
        },

        async deleteBranch(id) {
            try {
                await api.delete("/branches/"+id)
                showToast("Branch deleted successfully","success")
                await this.fetchBranches()
            } catch (error) {
                showToast(error.response?.data?.message || "Failed to delete branch","danger")
            }
        }
    }
}
</script>
