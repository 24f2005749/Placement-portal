<template>

<div class="card mb-3">
    <div class="card-body">
        <h5>
            {{ company.company_name }}
        </h5>
        <p>
            {{ company.website }}
        </p>
        <span class="badge bg-info">

            {{ company.approval_status }}

        </span>

    </div>
</div>

</template>

<script>

export default{
    props:["company"]
}

</script>