$(document).ready(function () {
    $('input[name="sys_static_head"]').val('0.49');
    $('input[name="sys_k_factor"]').val('2264.13');

    $('input[name="pump_0"]').val('120');
    $('input[name="pump_500"]').val('119');
    $('input[name="pump_1000"]').val('117');
    $('input[name="pump_1500"]').val('116');
    $('input[name="pump_2000"]').val('114');
    $('input[name="pump_2500"]').val('112');
    $('input[name="pump_3000"]').val('109');
    $('input[name="pump_3500"]').val('106');
    $('input[name="pump_4000"]').val('103');
    $('input[name="pump_4500"]').val('99');
    $('input[name="pump_5000"]').val('95');
    $('input[name="pump_5500"]').val('91');
    $('input[name="pump_6000"]').val('87');
    $('input[name="pump_6500"]').val('82');
    $('input[name="pump_7000"]').val('77');
    $('input[name="pump_7500"]').val('72');
    $('input[name="pump_8000"]').val('66');
    $('input[name="pump_8500"]').val('60');
    $('input[name="pump_9000"]').val('53');
    $('input[name="pump_9500"]').val('45');
    $('input[name="pump_10000"]').val('35');

    $("#submit-button").click(function () {
        var values = {};
        $('input').each(function () {
            key = $(this).attr('name');
            value = $(this).val();

            values[key] = value;
        });

        $(document).ajaxStart(function () {
            // show loader on start
            $("#loadbar").css("display", "block");
        }).ajaxSuccess(function () {
            // hide loader on success
            $("#loadbar").css("display", "none");
        });

        $.ajax({
            type: 'POST',
            url: `${window.location.protocol}//${window.location.host}/visualize`,
            data: JSON.stringify(values),
            success: function (data) {
                $('#result').html(`
                <div class="col-12 alert alert-success" role="alert">
                    <h2>Result</h2>
                    <p>
                        Flow: ${data['flow']}<br>Pump Pressure: ${data['pump_pressure']}
                    </p>
                    <div>
                        ${data['html_chart']}
                    </div>
                </div>`)
                // alert(`Flow: ${data['flow']}\nPump Pressure: ${data['pump_pressure']}`)
            },
            contentType: "application/json",
            dataType: 'json'
        });
    });
});