<template>
    <div class="card shadow-sm">
        <div class="card-header">
            <b>
                {{ title }}
            </b>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <slot name="head"></slot>
                        </tr>
                    </thead>
                    <tbody>
                        <slot name="body"></slot>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: ["title"]
}
</script>
