<template>
    <DashboardLayout>
        <PageTitle title="Drives" />

        <SearchBar @search="search" />

        <Loader v-if="loading" />
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <EmptyState
            v-else-if="drives.length === 0"
            message="No drives found."
        />

        <DashboardTable v-else title="Manage Drives">
            <template #head>
                <th>Drive</th>
                <th>Company</th>
                <th>Location</th>
                <th>Deadline</th>
                <th>Approval</th>
                <th>Status</th>
                <th>Actions</th>
            </template>

            <template #body>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.title }}</td>
                    <td>{{ drive.company }}</td>
                    <td>{{ drive.location || "Not provided" }}</td>
                    <td>{{ drive.application_deadline }}</td>
                    <td><StatusBadge :status="drive.approval_status" /></td>
                    <td><StatusBadge :status="drive.status" /></td>
                    <td>
                        <button
                            class="btn btn-success btn-sm me-2"
                            @click="updateDrive(drive, { approval_status: 'approved' })"
                            :disabled="drive.approval_status === 'approved' || updatingId === drive.id"
                        >
                            {{ updatingId === drive.id ? "Updating..." : "Approve" }}
                        </button>
                        <button
                            class="btn btn-outline-danger btn-sm me-2"
                            @click="updateDrive(drive, { approval_status: 'rejected' })"
                            :disabled="drive.approval_status === 'rejected' || updatingId === drive.id"
                        >
                            Reject
                        </button>
                        <button
                            class="btn btn-sm"
                            :class="drive.status === 'open' ? 'btn-outline-warning' : 'btn-outline-success'"
                            @click="updateDrive(drive, { status: drive.status === 'open' ? 'closed' : 'open' })"
                            :disabled="updatingId === drive.id"
                        >
                            {{ drive.status === "open" ? "Close" : "Open" }}
                        </button>
                    </td>
                </tr>
            </template>
        </DashboardTable>
    </DashboardLayout>
</template>

<script>
import api from "@/services/api"
import { showToast } from "@/utils/toast"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import SearchBar from "@/components/SearchBar.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import Loader from "@/components/Loader.vue"
import EmptyState from "@/components/EmptyState.vue"

export default {
    components: { DashboardLayout, DashboardTable, PageTitle, SearchBar, StatusBadge, Loader, EmptyState },

    data() {
        return {
            drives: [],
            allDrives: [],
            loading: true,
            error: "",
            updatingId: null
        }
    },

    async mounted() {
        await this.fetchDrives()
    },

    methods: {
        async fetchDrives() {
            this.loading = true
            this.error = ""

            try {
                const response = await api.get("/admin/drives")
                this.drives = response.data
                this.allDrives = response.data
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load drives"
            } finally {
                this.loading = false
            }
        },

        search(q) {
            const query = q.trim().toLowerCase()

            if(!query){
                this.drives = this.allDrives
                return
            }

            this.drives = this.allDrives.filter(drive =>
                drive.title.toLowerCase().includes(query) ||
                drive.company.toLowerCase().includes(query) ||
                (drive.location || "").toLowerCase().includes(query)
            )
        },

        async updateDrive(drive, changes) {
            this.updatingId = drive.id

            try {
                await api.put(`/admin/drives/${drive.id}`, {
                    approval_status: drive.approval_status,
                    status: drive.status || "open",
                    ...changes
                })
                showToast("Drive updated successfully", "success")
                await this.fetchDrives()
            } catch (error) {
                showToast(error.response?.data?.message || "Failed to update drive", "danger")
            } finally {
                this.updatingId = null
            }
        }
    }
}
</script>
