// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface SendEmailRequest {
  student_email: string
  student_name: string
  status: 'approved' | 'rejected'
  rejection_reason?: string
  college_name?: string
}

interface ResendEmailData {
  from: string
  to: string[]
  subject: string
  html: string
}

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')!
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/xanpndqw' // Fallback endpoint based on user preferences

Deno.serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { student_email, student_name, status, rejection_reason, college_name } = await req.json() as SendEmailRequest

    // Validate required fields
    if (!student_email || !student_name || !status) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields: student_email, student_name, status' }),
        { 
          status: 400, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    // Validate status
    if (!['approved', 'rejected'].includes(status)) {
      return new Response(
        JSON.stringify({ error: 'Status must be either "approved" or "rejected"' }),
        { 
          status: 400, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    // Generate email content based on status
    const emailContent = generateEmailContent(student_name, status, rejection_reason, college_name)
    
    let emailSent = false
    let response_data: any = null

    // Try Resend first (primary method)
    if (RESEND_API_KEY) {
      try {
        const emailData: ResendEmailData = {
          from: Deno.env.get('FROM_EMAIL') || 'noreply@collegeportal.com',
          to: [student_email],
          subject: emailContent.subject,
          html: emailContent.html
        }

        const resendResponse = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${RESEND_API_KEY}`,
          },
          body: JSON.stringify(emailData)
        })

        if (resendResponse.ok) {
          response_data = await resendResponse.json()
          emailSent = true
          console.log(`Email sent via Resend to ${student_email} for status: ${status}`)
        } else {
          const errorText = await resendResponse.text()
          console.error('Resend API error:', errorText)
          throw new Error(`Resend failed: ${resendResponse.status}`)
        }
      } catch (error) {
        console.error('Resend error:', error)
        // Continue to Formspree fallback
      }
    }

    // Fallback to Formspree (based on user preferences)
    if (!emailSent) {
      try {
        const formspreeData = {
          email: student_email,
          name: student_name,
          subject: emailContent.subject,
          message: emailContent.textContent,
          _replyto: student_email,
          _subject: emailContent.subject
        }

        const formspreeResponse = await fetch(FORMSPREE_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(formspreeData)
        })

        if (formspreeResponse.ok) {
          response_data = await formspreeResponse.json()
          emailSent = true
          console.log(`Email sent via Formspree fallback to ${student_email} for status: ${status}`)
        } else {
          const errorText = await formspreeResponse.text()
          console.error('Formspree API error:', errorText)
          throw new Error(`Formspree failed: ${formspreeResponse.status}`)
        }
      } catch (error) {
        console.error('Formspree fallback error:', error)
      }
    }

    if (!emailSent) {
      return new Response(
        JSON.stringify({ 
          error: 'Failed to send email via both Resend and Formspree',
          details: 'All email providers failed'
        }),
        { 
          status: 500, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    return new Response(
      JSON.stringify({ 
        message: 'Email sent successfully',
        recipient: student_email,
        status: status,
        provider: RESEND_API_KEY ? 'resend' : 'formspree',
        data: response_data
      }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    )

  } catch (error) {
    console.error('Error in send-status-email function:', error)
    return new Response(
      JSON.stringify({ 
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      }),
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})

function generateEmailContent(
  studentName: string, 
  status: 'approved' | 'rejected', 
  rejectionReason?: string,
  collegeName: string = 'College Placement Portal'
) {
  const baseStyles = `
    <style>
      body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
      .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
      .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
      .status-approved { color: #22c55e; font-weight: bold; font-size: 18px; }
      .status-rejected { color: #ef4444; font-weight: bold; font-size: 18px; }
      .reason-box { background: #fee2e2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; border-radius: 5px; }
      .next-steps { background: #ecfdf5; border-left: 4px solid #22c55e; padding: 15px; margin: 20px 0; border-radius: 5px; }
      .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
      .cta-button { display: inline-block; background: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
  `

  if (status === 'approved') {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        ${baseStyles}
      </head>
      <body>
        <div class="header">
          <h1>🎉 Account Approved!</h1>
          <p>Welcome to ${collegeName}</p>
        </div>
        <div class="content">
          <p>Dear <strong>${studentName}</strong>,</p>
          
          <p>Great news! Your account registration has been <span class="status-approved">APPROVED</span>.</p>
          
          <div class="next-steps">
            <h3>🚀 What's Next?</h3>
            <ul>
              <li>You can now log in to access the placement portal</li>
              <li>Complete your profile with additional details</li>
              <li>Browse available placement opportunities</li>
              <li>Take practice assessments to prepare</li>
            </ul>
          </div>
          
          <p style="text-align: center;">
            <a href="${Deno.env.get('PORTAL_URL') || 'https://your-portal.com'}/login" class="cta-button">
              Access Portal Now
            </a>
          </p>
          
          <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
          
          <p>Best regards,<br>
          <strong>${collegeName} Team</strong></p>
        </div>
        <div class="footer">
          <p>This is an automated message. Please do not reply to this email.</p>
          <p>© ${new Date().getFullYear()} ${collegeName}. All rights reserved.</p>
        </div>
      </body>
      </html>
    `
    
    const textContent = `Dear ${studentName},

Great news! Your account registration has been APPROVED.

What's Next?
- You can now log in to access the placement portal
- Complete your profile with additional details
- Browse available placement opportunities
- Take practice assessments to prepare

Best regards,
${collegeName} Team`

    return {
      subject: `🎉 Congratulations! Your account has been approved - ${collegeName}`,
      html,
      textContent
    }
  } else {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        ${baseStyles}
      </head>
      <body>
        <div class="header">
          <h1>Application Status Update</h1>
          <p>${collegeName}</p>
        </div>
        <div class="content">
          <p>Dear <strong>${studentName}</strong>,</p>
          
          <p>Thank you for your interest in joining ${collegeName}. After careful review, we regret to inform you that your account registration has been <span class="status-rejected">NOT APPROVED</span> at this time.</p>
          
          ${rejectionReason ? `
            <div class="reason-box">
              <h3>📝 Reason for Decision:</h3>
              <p>${rejectionReason}</p>
            </div>
          ` : ''}
          
          <div class="next-steps">
            <h3>💡 What You Can Do:</h3>
            <ul>
              <li>Review the reason provided above (if applicable)</li>
              <li>Address any issues mentioned in the feedback</li>
              <li>You may reapply after addressing the concerns</li>
              <li>Contact our admissions team for clarification if needed</li>
            </ul>
          </div>
          
          <p>We encourage you to reapply once you've addressed the mentioned concerns. Our admissions team is always here to help guide you through the process.</p>
          
          <p>For any questions or to discuss your application, please contact us at:</p>
          <p><strong>Email:</strong> supreethvennila@gmail.com<br>
          <strong>Phone:</strong> +1 (555) 123-4567</p>
          
          <p>Best regards,<br>
          <strong>${collegeName} Admissions Team</strong></p>
        </div>
        <div class="footer">
          <p>This is an automated message. Please do not reply to this email.</p>
          <p>© ${new Date().getFullYear()} ${collegeName}. All rights reserved.</p>
        </div>
      </body>
      </html>
    `
    
    const textContent = `Dear ${studentName},

Thank you for your interest in joining ${collegeName}. After careful review, we regret to inform you that your account registration has been NOT APPROVED at this time.

${rejectionReason ? `Reason: ${rejectionReason}

` : ''}What You Can Do:
- Review the reason provided above (if applicable)
- Address any issues mentioned in the feedback
- You may reapply after addressing the concerns
- Contact our admissions team for clarification if needed

Best regards,
${collegeName} Admissions Team`

    return {
      subject: `Application Status Update - ${collegeName}`,
      html,
      textContent
    }
  }
}

/* To deploy this function:
1. Install Supabase CLI: npm install -g supabase
2. Login: supabase login
3. Link project: supabase link --project-ref your-project-ref
4. Deploy: supabase functions deploy send-status-email
5. Set environment variables:
   supabase secrets set RESEND_API_KEY=your_resend_api_key
   supabase secrets set FROM_EMAIL=supreethvennila@gmail.com
   supabase secrets set FROM_NAME="College Placement Portal"
   supabase secrets set PORTAL_URL=https://your-portal-url.com
*/