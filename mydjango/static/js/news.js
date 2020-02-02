$(function () {
    $('#newsFormModal').on('shown.bs.modal',function () {
        $('#newsInput').trigger('focus')    // 自动聚焦
    });
})
