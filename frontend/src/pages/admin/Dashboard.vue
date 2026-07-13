<template>
    <DashboardLayout>
        <PageTitle title="Admin Dashboard" />
        <Loader v-if="loading" />
        <div v-else>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div class="row g-3">
                <div class="col-md-3">
                    <StatCard title="Students" :value="dashboard.students" />
                </div>
                <div class="col-md-3">
                    <StatCard title="Companies" :value="dashboard.companies" />
                </div>
                <div class="col-md-3">
                    <StatCard title="Drives" :value="dashboard.drives" />
                </div>
                <div class="col-md-3">
                    <StatCard title="Applications" :value="dashboard.applications" />
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <DashboardTable title="Pending Companies">
                        <template #head>
                            <th>Name</th>
                            <th>Status</th>
                            <th></th>
                        </template>
                        <template #body>
                            <tr v-for="company in pendingCompanies" :key="company.id">
                                <td>
                                    {{ company.company_name }}
                                </td>
                                <td>
                                    <StatusBadge :status="company.approval_status" />
                                </td>
                                <td>
                                    <button class="btn btn-success btn-sm" @click="approveCompany(company.id)"
                                        :disabled="approvingId == company.id">
                                        {{ approvingId == company.id ? "Approving..." : "Approve" }}
                                    </button>
                                </td>
                            </tr>
                        </template>
                    </DashboardTable>
                </div>
                <div class="col-md-6">
                    <DashboardTable title="Pending Drives">
                        <template #head>
                            <th>Drive</th>
                            <th>Company</th>
                            <th></th>
                        </template>
                        <template #body>
                            <tr v-for="drive in pendingDrives" :key="drive.id">
                                <td>
                                    {{ drive.title }}
                                </td>
                                <td>
                                    {{ drive.company }}
                                </td>
                                <td>
                                    <button class="btn btn-success btn-sm" @click="approveDrive(drive.id)"
                                        :disabled="approvingId == drive.id">
                                        {{ approvingId == drive.id ? "Approving..." : "Approve" }}
                                    </button>
                                </td>
                            </tr>
                        </template>
                    </DashboardTable>
                </div>
            </div>
        </div>
    </DashboardLayout>
</template>
<script>
import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import DashboardTable from "@/components/DashboardTable.vue"
import PageTitle from "@/components/PageTitle.vue"
import StatCard from "@/components/StatCard.vue"
import StatusBadge from "@/components/StatusBadge.vue"
import Loader from "@/components/Loader.vue"
import { showToast } from "@/utils/toast"
export default {
    components: {
        DashboardLayout,
        DashboardTable,
        PageTitle,
        StatCard,
        StatusBadge,
        Loader
    },
    data() {
        return {
            dashboard: {},
            pendingCompanies: [],
            pendingDrives: [],
            loading: true,
            error: "",
            approvingId: null
        }
    },
    async mounted() {
        await this.loadDashboard()
    },
    methods: {
        async loadDashboard() {
            this.loading = true
            this.error = ""
            try {
                const response = await api.get("/admin/dashboard")
                this.dashboard = response.data
                const companiesResponse = await api.get("/admin/companies")
                const drivesResponse = await api.get("/admin/drives")
                this.pendingCompanies = companiesResponse.data.filter(
                    company => company.approval_status == "pending"
                )
                this.pendingDrives = drivesResponse.data.filter(
                    drive => drive.approval_status == "pending"
                )
            }
            catch (error) {
                this.error = error.response?.data?.message || "Failed to load dashboard"
                console.error(error)
            }
            finally {
                this.loading = false
            }
        },
        async approveCompany(id) {
            this.approvingId = id
            try {
                await api.put("/admin/companies/" + id, {
                    approval_status: "approved"
                })
                await this.loadDashboard()
                showToast("Company approved successfully", "success")
            }
            catch (error) {
                this.error = error.response?.data?.message || "Failed to approve company"
            }
            finally {
                this.approvingId = null
            }
        },
        async approveDrive(id) {
            this.approvingId = id
            try {
                await api.put("/admin/drives/" + id, {
                    approval_status: "approved"
                })
                await this.loadDashboard()
                showToast("Drive approved successfully", "success")
            }
            catch (error) {
                this.error = error.response?.data?.message || "Failed to approve drive"
            }
            finally {
                this.approvingId = null
            }
        }
    }
}
</script>
