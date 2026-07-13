<template>
    <div class="modal fade show d-block" style="background:rgba(0,0,0,.5)">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5>
                        Update Application
                    </h5>
                    <button class="btn-close" @click="$emit('close')" />
                </div>

                <div class="modal-body">
                    <label>Status</label>
                    <select v-model="status" class="form-select mb-3">
                        <option>applied</option>
                        <option>shortlisted</option>
                        <option>selected</option>
                        <option>rejected</option>
                    </select>
                    <label>Interview Date</label>
                    <input v-model="interview_date" type="datetime-local" class="form-control mb-3"
                        :disabled="status === 'rejected'">
                    <label>Remarks</label>
                    <textarea v-model="remarks" class="form-control mb-3"></textarea>
                    <button class="btn btn-success" @click="save">
                        Save
                    </button>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import api from "@/services/api"
export default {
    props: ["application"],
    data() {
        return {
            status: "",
            remarks: "",
            interview_date: ""
        }
    },
    mounted() {
        this.status = this.application.status
        this.remarks = this.application.remarks
        this.interview_date = this.application.interview_date
    },
    methods: {
        async save() {
            try {
                let interview_date_formatted = this.interview_date
                if (this.status === "rejected") {
                    interview_date_formatted = null
                }
                else if (this.interview_date) {
                    interview_date_formatted = this.interview_date.slice(0, 16).replace("T", " ")
                }
                await api.put(
                    "/company/applications/" + this.application.application_id,
                    {
                        status: this.status,
                        remarks: this.remarks,
                        interview_date: interview_date_formatted
                    }
                )
                this.$emit("updated")
                this.$emit("close")
            }
            catch (error) {
                alert(error.response?.data?.message || "Failed to update application")
            }
        }
    }
}
</script>
